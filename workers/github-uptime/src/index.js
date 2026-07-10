const GITHUB_ACCOUNT_CREATED_AT = Date.UTC(2021, 10, 20, 13, 52, 28);
const SVG_HEADERS = {
  "Content-Type": "image/svg+xml; charset=utf-8",
  "Cache-Control": "no-store, max-age=0, must-revalidate",
  "CDN-Cache-Control": "no-store",
  "Pragma": "no-cache",
  "Expires": "0",
  "X-Content-Type-Options": "nosniff",
};

export default {
  fetch(request) {
    const url = new URL(request.url);
    if (url.pathname !== "/" && url.pathname !== "/uptime.svg") {
      return new Response("Not found", { status: 404 });
    }
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method not allowed", {
        status: 405,
        headers: { Allow: "GET, HEAD" },
      });
    }

    const elapsedSeconds = Math.max(
      0,
      Math.floor((Date.now() - GITHUB_ACCOUNT_CREATED_AT) / 1000),
    );
    return new Response(request.method === "HEAD" ? null : renderSvg(elapsedSeconds), {
      headers: SVG_HEADERS,
    });
  },
};

function renderSvg(elapsedSeconds) {
  const formatted = elapsedSeconds.toLocaleString("en-US");
  const number = String(elapsedSeconds).padStart(9, "0").slice(-9);
  const digitStyles = Array.from({ length: 9 }, (_, index) => {
    const place = 8 - index;
    const period = 10 ** (place + 1);
    const delay = elapsedSeconds % period;
    return `.d${place}::after{content:"${number[index]}";animation-duration:${period}s;animation-delay:-${delay}s}`;
  }).join("");

  return `<svg xmlns="http://www.w3.org/2000/svg" width="176" height="24" viewBox="0 0 176 24" role="img" aria-labelledby="title desc">
  <title id="title">Live GitHub account uptime</title>
  <desc id="desc">${formatted} elapsed seconds since 20 November 2021 at 13:52:28 UTC. The counter advances every second.</desc>
  <style>
    .panel{fill:#0d1117;stroke:#30363d;stroke-width:1}.screen{color:#39d353;font:700 14px ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,\"Liberation Mono\",monospace;line-height:24px;white-space:nowrap}.digit::after{content:\"0\";display:inline-block;width:.61em;animation-name:roll;animation-timing-function:step-end;animation-iteration-count:infinite;animation-fill-mode:both}.comma{display:inline-block;width:.34em}.unit{color:#8b949e;margin-left:.15em;font-weight:500}${digitStyles}@keyframes roll{0%,9.999%{content:\"0\"}10%,19.999%{content:\"1\"}20%,29.999%{content:\"2\"}30%,39.999%{content:\"3\"}40%,49.999%{content:\"4\"}50%,59.999%{content:\"5\"}60%,69.999%{content:\"6\"}70%,79.999%{content:\"7\"}80%,89.999%{content:\"8\"}90%,99.999%{content:\"9\"}100%{content:\"0\"}}
  </style>
  <rect class="panel" x=".5" y=".5" width="175" height="23" rx="4"/>
  <foreignObject x="7" y="0" width="162" height="24">
    <div xmlns="http://www.w3.org/1999/xhtml" class="screen" aria-label="Live GitHub uptime in elapsed seconds"><span class="digit d8"></span><span class="digit d7"></span><span class="digit d6"></span><span class="comma">,</span><span class="digit d5"></span><span class="digit d4"></span><span class="digit d3"></span><span class="comma">,</span><span class="digit d2"></span><span class="digit d1"></span><span class="digit d0"></span><span class="unit">s</span></div>
  </foreignObject>
</svg>`;
}
