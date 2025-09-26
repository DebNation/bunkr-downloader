// const data = {
//   encrypted: true,
//   timestamp: 1758629240,
//   url: "OzE3IjZucGQnPDpGFlpAXlMhazEnajU7KSRub1EBFQAGXmpod2pzbXIpJGA9GQ0MDVFdMScgZHBlZmUoKWs="
// };
async function main() {
  const args = process.argv.slice(2);
  let url = args[0]; 
  const finalUrlResp = await getFinalUrl(url);
  let finalURL = "";
  if (finalUrlResp.encrypted != false) {
    finalURL = decryptUrl(finalUrlResp.url, finalUrlResp.timestamp);
  } else {
    finalURL = finalUrlResp.url;
  }
  let title = await getTitle(url);
  let finalDownloadUrl = `${finalURL}?n=${title}`;
  console.log(finalDownloadUrl);
}

async function getFinalUrl(url) {
  const slug = url.split("/").pop();
  try {
    let response = await fetch("https://bunkr.cr/api/vs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ slug }),
    });
    let json = await response.json();
    return json;
  } catch (error) {
    console.error("Error:", error);
  }
}

function decryptUrl(base64Url, timestamp) {
  const binary = Buffer.from(base64Url, "base64");
  const key = `SECRET_KEY_${Math.floor(timestamp / 3600)}`;
  const keyBytes = new TextEncoder().encode(key);

  const output = [];
  for (let i = 0; i < binary.length; i++) {
    output.push(binary[i] ^ keyBytes[i % keyBytes.length]);
  }
  return Buffer.from(output).toString("utf8");
}

async function getTitle(url) {
  try {
    let response = await fetch(url);
    let html = await response.text();
    const match = html.match(/<title>(.*?)<\/title>/i);
    if (match) {
      const filename = match[1].replace(" | Bunkr", "").trim();
      const encoded_title = encodeURIComponent(filename);
      return encoded_title;
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

main();
