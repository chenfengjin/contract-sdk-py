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
        init_args: { "creator": "xchain"},
        options:{"account":"xchain"}
    });
}
//
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
    console.log(resp.Message)
})


Test("Iterator",function (t) {
    var c = deploy();
    c.Invoke("Increase",{"key":"key1"})
    c.Invoke("Increase",{"key":"key2"})
    c.Invoke("Increase",{"key":"key3"})
    c.Invoke("Increase",{"key":"key4"})
    var resp = c.Invoke("RangeList",{"start":"key2","limit":"key4"})
    console.log(resp.Body)
    console.log(resp.Message)
})


Test("PrefixIterator",function (t) {
    var c = deploy();
    c.Invoke("Increase",{"key":"key1"})
    c.Invoke("Increase",{"key":"key2"})
    c.Invoke("Increase",{"key":"key3"})
    c.Invoke("Increase",{"key":"key4"})
    c.Invoke("Increase",{"key":"keyy"})
    c.Invoke("Increase",{"key":"kew"})

    var resp = c.Invoke("PrefixList",{"prefix":"key"})
    assert.deepStrictEqual(JSON.parse(resp.Body),[{"key": "key1", "value": "1"}, {"key": "key2", "value": "1"}, {"key": "key3", "value": "1"}, {"key": "key4", "value": "1"}, {"key": "keyy", "value": "1"}])
    {
        c.Invoke("Delete",{"key":"keyy"})
    }
    var resp = c.Invoke("PrefixList",{"prefix":"key"})
    //TODO @fengjin
    // assert.deepStrictEqual(JSON.parse(resp.Body),[{"key": "key1", "value": "1"}, {"key": "key2", "value": "1"}, {"key": "key3", "value": "1"}, {"key": "key4", "value": "1"}])

})

Test("C2",function (t) {
        c2 =  xchain.Deploy({
        name: "c2",
        code: "../call/c2.py",
        lang: lang,
        type: type,
        init_args: { "creator": "xchain" }
    });
        // resp = c2.Invoke("invoke",{})
        // console.log(resp.Body)

        c1 =  xchain.Deploy({
        name: "c1",
        code: "../call/c1.py",
        lang: lang,
        type: type,
        init_args: { "creator": "xchain" }
    });
        var resp = c1.Invoke("invoke",{"contract":"c2"})
    console.log("from c1:"+resp.Body)
    // console.log(resp.Message)
    // console.log(resp.Status)
})