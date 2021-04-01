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

Test("Increase", function (t) {
    var c = deploy();
    var resp = c.Invoke("Increase", { "key": "xchain" });
    console.log(resp.Message)
    console.log(resp.Body)
    // assert.equal(resp.Body, "1");
    // var resp = c.Invoke("Increase", { "key": "xchain" });
    // assert.equal(resp.Body,"2")
    // var resp = c.Invoke("Get",{"key":"xchain"})
    // assert.equal(resp.Body,"2")
})

// Test("Get", function (t) {
//     var c = deploy()
//     c.Invoke("Increase", { "key": "xchain" });
//     var resp = c.Invoke("Get", { "key": "xchain" })
//     console.log(resp.Message)
//     console.log(resp.Body)
//     // assert.equal(resp.Body, "1")
// })