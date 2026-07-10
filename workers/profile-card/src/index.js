const GITHUB_ACCOUNT_CREATED_AT = new Date(Date.UTC(2021, 10, 20, 13, 52, 28));
const RAW_CARD_BASE =
  "https://raw.githubusercontent.com/Samthesurf/Samthesurf/main/assets/profile-";

const SVG_HEADERS = {
  "Content-Type": "image/svg+xml; charset=utf-8",
  "Cache-Control": "no-store, max-age=0, must-revalidate",
  "CDN-Cache-Control": "no-store",
  "Cloudflare-CDN-Cache-Control": "no-store",
  Pragma: "no-cache",
  Expires: "0",
  "Access-Control-Allow-Origin": "*",
  "X-Content-Type-Options": "nosniff",
};

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const mode = modeFromPath(url.pathname);

    if (!mode) {
      return new Response("Not found", { status: 404 });
    }
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method not allowed", {
        status: 405,
        headers: { Allow: "GET, HEAD" },
      });
    }
    if (request.method === "HEAD") {
      return new Response(null, { headers: SVG_HEADERS });
    }

    try {
      const templateResponse = await fetch(`${RAW_CARD_BASE}${mode}.svg`, {
        headers: { "User-Agent": "samthesurf-live-profile-card" },
        cf: { cacheTtl: 60, cacheEverything: true },
      });
      if (!templateResponse.ok) {
        throw new Error(`Template fetch failed with ${templateResponse.status}`);
      }

      const template = await templateResponse.text();
      const now = new Date();
      const age = calendarAge(GITHUB_ACCOUNT_CREATED_AT, now);
      const svg = injectLiveUptime(template, age, mode, now);

      return new Response(svg, { headers: SVG_HEADERS });
    } catch (error) {
      return new Response(`Unable to render profile card: ${error.message}`, {
        status: 502,
        headers: {
          "Content-Type": "text/plain; charset=utf-8",
          "Cache-Control": "no-store",
        },
      });
    }
  },
};

function modeFromPath(pathname) {
  if (pathname === "/" || pathname === "/dark.svg") return "dark";
  if (pathname === "/light.svg") return "light";
  return null;
}

function injectLiveUptime(template, age, mode, now) {
  const textColor = mode === "dark" ? "#c9d1d9" : "#24292f";
  const fraction = now.getUTCMilliseconds() / 1000;
  const secondPhase = age.seconds + fraction;
  const minutePhase = age.minutes * 60 + secondPhase;
  const hourPhase = age.hours * 3600 + minutePhase;
  const readable = `${age.years}y ${age.months}mo ${age.days}d ${age.hours}h ${age.minutes}m ${age.seconds}s`;

  const liveMarkup = `<foreignObject id="uptime-value" x="548" y="184" width="310" height="24">
    <div xmlns="http://www.w3.org/1999/xhtml" class="live-uptime" aria-label="GitHub account uptime: ${readable}">
      <span>${age.years}y ${age.months}mo ${age.days}d </span><span class="reel hours"></span><span>h </span><span class="reel minutes"></span><span>m </span><span class="reel seconds"></span><span>s</span>
    </div>
    <style xmlns="http://www.w3.org/1999/xhtml">
      .live-uptime{color:${textColor};font:14px/24px ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono",monospace;white-space:nowrap}
      .reel::after{display:inline-block;min-width:1.2em;text-align:right;animation-timing-function:step-end;animation-iteration-count:infinite;animation-fill-mode:both}
      .seconds::after{content:"${pad2(age.seconds)}";animation-name:roll60;animation-duration:60s;animation-delay:-${secondPhase.toFixed(3)}s}
      .minutes::after{content:"${pad2(age.minutes)}";animation-name:roll60;animation-duration:3600s;animation-delay:-${minutePhase.toFixed(3)}s}
      .hours::after{content:"${pad2(age.hours)}";animation-name:roll24;animation-duration:86400s;animation-delay:-${hourPhase.toFixed(3)}s}
      ${contentKeyframes("roll60", 60)}
      ${contentKeyframes("roll24", 24)}
    </style>
  </foreignObject>`;

  const uptimePattern = /<text(?: id="uptime-value")? x="548" y="201"[^>]*>.*?<\/text>/;
  if (!uptimePattern.test(template)) {
    throw new Error("Uptime placeholder was not found in the profile card template");
  }

  return template
    .replace(uptimePattern, liveMarkup)
    .replace(
      /<desc id="desc">.*?<\/desc>/,
      `<desc id="desc">Samuel Ukpai's live GitHub profile card. Account uptime is ${readable} at load time and advances every second.</desc>`,
    );
}

function contentKeyframes(name, count) {
  const frames = [];
  for (let value = 0; value < count; value += 1) {
    const start = ((value / count) * 100).toFixed(6);
    const end = ((((value + 1) / count) * 100) - 0.000001).toFixed(6);
    frames.push(`${start}%,${end}%{content:"${pad2(value)}"}`);
  }
  frames.push(`100%{content:"00"}`);
  return `@keyframes ${name}{${frames.join("")}}`;
}

function calendarAge(start, now) {
  let years = now.getUTCFullYear() - start.getUTCFullYear();
  let cursor = addYearsUtc(start, years);
  if (cursor > now) {
    years -= 1;
    cursor = addYearsUtc(start, years);
  }

  let months =
    (now.getUTCFullYear() - cursor.getUTCFullYear()) * 12 +
    now.getUTCMonth() -
    cursor.getUTCMonth();
  let candidate = addMonthsUtc(cursor, months);
  if (candidate > now) {
    months -= 1;
    candidate = addMonthsUtc(cursor, months);
  }
  cursor = candidate;

  let remaining = Math.max(0, Math.floor((now.getTime() - cursor.getTime()) / 1000));
  const days = Math.floor(remaining / 86400);
  remaining %= 86400;
  const hours = Math.floor(remaining / 3600);
  remaining %= 3600;
  const minutes = Math.floor(remaining / 60);
  const seconds = remaining % 60;

  return { years, months, days, hours, minutes, seconds };
}

function addYearsUtc(date, years) {
  const year = date.getUTCFullYear() + years;
  const month = date.getUTCMonth();
  const day = Math.min(date.getUTCDate(), daysInMonthUtc(year, month));
  return new Date(
    Date.UTC(
      year,
      month,
      day,
      date.getUTCHours(),
      date.getUTCMinutes(),
      date.getUTCSeconds(),
      date.getUTCMilliseconds(),
    ),
  );
}

function addMonthsUtc(date, months) {
  const absoluteMonth = date.getUTCMonth() + months;
  const year = date.getUTCFullYear() + Math.floor(absoluteMonth / 12);
  const month = ((absoluteMonth % 12) + 12) % 12;
  const day = Math.min(date.getUTCDate(), daysInMonthUtc(year, month));
  return new Date(
    Date.UTC(
      year,
      month,
      day,
      date.getUTCHours(),
      date.getUTCMinutes(),
      date.getUTCSeconds(),
      date.getUTCMilliseconds(),
    ),
  );
}

function daysInMonthUtc(year, month) {
  return new Date(Date.UTC(year, month + 1, 0)).getUTCDate();
}

function pad2(value) {
  return String(value).padStart(2, "0");
}
