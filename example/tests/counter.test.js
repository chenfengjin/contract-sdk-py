var assert = require("assert");

var codePath = "../counter/counter.py";

var lang = "py"
var type = "native"
function deploy() {
    return xchain.Deploy({
        name: "counter",
        code: codePath,
        lang: lang,
        type: type,
        init_args: { "creator": "xchain" }
    });
}
//
// Test("Increase", function (t) {
//     var c = deploy();
//
//     var resp = c.Invoke("Increase", { "key": "key" });
//     console.log(resp.Message)
//     console.log(resp.Body)
//     assert.equal(resp.Body, "1");
//     var resp = c.Invoke("Get",{"key":"key"})
//     assert.equal(resp.Body,"1")
//     var resp = c.Invoke("Caller", { "key": "xchain" },{"account":"xchain"});
//     assert.equal(resp.Body,"xchain")
//     // console.log(resp.Body)
// })


Test("Iterator",function (t) {
    var c = deploy();
    c.Invoke("Increase",{"key":"key1"})
    c.Invoke("Increase",{"key":"key2"})
    c.Invoke("Increase",{"key":"key3"})
    c.Invoke("Increase",{"key":"key4"})
    var resp = c.Invoke("List",{"start":"key2","limit":"key4"})
    console.log(resp.Body)
    console.log(resp.Message)
})

// Test("Get", function (t) {
//     var c = deploy()
//     c.Invoke("Increase", { "key": "xchain" });
//     var resp = c.Invoke("Get", { "key": "xchain" })
//     console.log(resp.Message)
//     console.log(resp.Body)
//     // assert.equal(resp.Body, "1")
// })