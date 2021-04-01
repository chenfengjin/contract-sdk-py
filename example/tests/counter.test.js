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

    var resp = c.Invoke("Increase", { "key": "key" });
    console.log(resp.Message)
    console.log(resp.Body)
    assert.equal(resp.Body, "1");
        var resp = c.Invoke("Get",{"key":"key"})
    assert.equal(resp.Body,"1")
    var resp = c.Invoke("Caller", { "key": "xchain" },{"account":"xchain"});
    assert.equal(resp.Body,"xchain")
    // console.log(resp.Body)
})


// Test("Get", function (t) {
//     var c = deploy()
//     c.Invoke("Increase", { "key": "xchain" });
//     var resp = c.Invoke("Get", { "key": "xchain" })
//     console.log(resp.Message)
//     console.log(resp.Body)
//     // assert.equal(resp.Body, "1")
// })