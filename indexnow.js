const axios = require("axios");
const fs = require("fs");

const key = "puadh12345indexnow";
const host = "puadhpunjabipodcast.com";

const urls = fs.readFileSync("urls.txt", "utf-8")
  .split("\n")
  .map(u => u.trim())
  .filter(u => u);

axios.post("https://api.indexnow.org/indexnow", {
  host: host,
  key: key,
  urlList: urls
})
.then(res => console.log("✅ Submitted:", res.status))
.catch(err => console.error("❌ Error:", err.response?.data || err.message));