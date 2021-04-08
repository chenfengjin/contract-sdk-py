var assert = require("assert");

var codePath = "../features/features.py";

var lang = "py"
var type = "native"

function deploy() {
    return xchain.Deploy({
        name: "features",
        code: codePath,
        lang: lang,
        type: type,
        init_args: {"creator": "xchain"},
        options: {"account": "xchain"}
    });
}

//
Test("Log", function (t) {
    var c = deploy();
    var resp = c.Invoke("Log", {});
    assert.equal(resp.Body, "ok")
})

Test("QueryTx",function(t){
    var c = deploy()
    var resp = c.Invoke("QueryTx",{"txid":""})
})
