// run in devtools console
((x) => {
const a = document.createElement("a");
a.href = URL.createObjectURL(new Blob([JSON.stringify(x, undefined, 4)],{type:"application/json;charset=utf-8;"}));
a.setAttribute('download','headers.json');
a.click();
})({
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Cookie': document.cookie,
    'User-Agent': navigator.userAgent,
})