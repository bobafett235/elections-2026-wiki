import { test, expect } from "@playwright/test"
import { createServer } from "node:http"
import { once } from "node:events"
import { resolve } from "node:path"
import serveHandler from "serve-handler"

const prefix = "/elections-2026-wiki"
let baseUrl = process.env.WIKI_BASE_URL
let server

test.use({ viewport: { width: 1440, height: 1000 } })

test.beforeAll(async () => {
  if (baseUrl) return

  // Exercise the production build under its GitHub Pages subpath. Quartz's
  // --serve mode deliberately clears basepath and would conceal this bug.
  server = createServer((request, response) => {
    const url = new URL(request.url, "http://localhost")
    if (!url.pathname.startsWith(`${prefix}/`)) {
      response.writeHead(404)
      response.end("Outside the published wiki path")
      return
    }
    request.url = `${url.pathname.slice(prefix.length)}${url.search}`
    return serveHandler(request, response, {
      public: resolve("public"),
      cleanUrls: true,
    })
  })
  server.listen(0, "127.0.0.1")
  await once(server, "listening")
  baseUrl = `http://127.0.0.1:${server.address().port}${prefix}/`
})

test.afterAll(async () => {
  if (server) await new Promise((done) => server.close(done))
})

test("explorer opens Annie Andrews and preserves the site prefix during navigation", async ({
  page,
}) => {
  const initial = await page.goto(baseUrl)
  expect(initial.status()).toBe(200)
  const annie = page.locator('.explorer a[href$="/pages/entities/annie-andrews"]')
  await expect(annie).toHaveCount(1)
  for (const folder of ["pages/index", "pages/entities/index"]) {
    if (!(await annie.isVisible())) {
      await page.locator(`.explorer [data-folderpath="${folder}"] .folder-icon`).click()
    }
  }

  const navigationResponse = page.waitForResponse((response) =>
    response.url().endsWith("/pages/entities/annie-andrews"),
  )
  await annie.click()
  expect((await navigationResponse).status()).toBe(200)
  await expect(page).toHaveURL(new URL("pages/entities/annie-andrews", baseUrl).href)
  await expect(page.locator("article h1")).toHaveText("Annie Andrews")

  // The next explorer click runs from a nested page after SPA navigation.
  await page.locator('.explorer a[href$="/pages/entities/ralph-norman"]').click()
  await expect(page).toHaveURL(new URL("pages/entities/ralph-norman", baseUrl).href)
  await expect(page.locator("article h1")).toHaveText("Ralph Norman")
  await page.goBack()
  await expect(page).toHaveURL(new URL("pages/entities/annie-andrews", baseUrl).href)
  await expect(page.locator("article h1")).toHaveText("Annie Andrews")
})

test("every explorer file and folder resolves inside the published wiki", async ({
  page,
  request,
}, testInfo) => {
  test.setTimeout(120_000)
  await page.goto(baseUrl)
  const indexResponse = await request.get(new URL("static/contentIndex.json", baseUrl).href)
  expect(indexResponse.status()).toBe(200)
  const index = await indexResponse.json()
  // Quartz indexes generated folder/tag pages too; the explorer hides tags
  // and renders folder indexes as folder links rather than file entries.
  const explorerSlugs = Object.keys(index).filter(
    (slug) => slug !== "index" && !slug.startsWith("tags/"),
  )
  const expectedFiles = explorerSlugs.filter((slug) => !slug.endsWith("/index"))
  await expect(page.locator(".explorer a.nav-file-title")).toHaveCount(expectedFiles.length)

  const links = await page
    .locator(".explorer a[href]")
    .evaluateAll((elements) => [...new Set(elements.map((element) => element.href))].sort())
  const site = new URL(baseUrl)
  for (const link of links) {
    const url = new URL(link)
    expect(url.origin, link).toBe(site.origin)
    expect(url.pathname, link).toMatch(/^\/elections-2026-wiki\//)
  }
  expect(links).toHaveLength(explorerSlugs.length)
  for (const slug of explorerSlugs) {
    const path = slug.endsWith("/index") ? slug.slice(0, -5) : slug
    expect(links).toContain(new URL(path, baseUrl).href)
  }

  const results = []
  for (let offset = 0; offset < links.length; offset += 6) {
    results.push(
      ...(await Promise.all(
        links.slice(offset, offset + 6).map(async (url) => {
          const response = await request.get(url)
          return { url, status: response.status() }
        }),
      )),
    )
  }
  await testInfo.attach("explorer-link-results", {
    body: JSON.stringify(results, null, 2),
    contentType: "application/json",
  })
  expect(results.filter(({ status }) => status !== 200)).toEqual([])
  console.log(
    `Verified ${results.length} explorer links (${expectedFiles.length} files plus folders)`,
  )
})
