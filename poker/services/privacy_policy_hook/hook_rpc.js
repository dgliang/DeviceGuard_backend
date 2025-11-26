console.log("Frida Script loaded successfully ");
Java.perform(function x() {
    // hook Intent之间传递的url
    var act = Java.use("android.content.Intent");

    act.getData.implementation = function() {
        var data = this.getData()
        var extra = this.getExtras()
        send("getData");
        send(data)
        send(extra.toString())
        send(this.toUri(256))
//        send({"type":"Intent.Data", "data":data})
//        send({"type":"Intent.Extra", "bb":extra.toString()})
//        send({"type":"Intent.URI", "cc":this.toUri(256)})
        return data
    };

    act.setData.implementation = function(data) {
        send("setData");
        send(this.toUri(256));
//        send({"type":"Intent.Data", "data":data})
//        send({"type":"Intent.Extra", "bb":extra.toString()})
//        send({"type":"Intent.URI", "cc":this.toUri(256)})
        this.setData(data);
    };

    // hook startActivity传递的url
    var Activity = Java.use("android.app.Activity");
    Activity.startActivity.overload('android.content.Intent').implementation=function(p1){
        send("startActivity");
        var data = decodeURIComponent(p1.toUri(256))
        send(data)
//        send({"type":"startActivity1.Data", "data":data})
        this.startActivity(p1);
    }
    Activity.startActivity.overload('android.content.Intent', 'android.os.Bundle').implementation=function(p1,p2){
        send("startActivity2");
        var data = decodeURIComponent(p1.toUri(256))
        send(data)
//        send({"type":"startActivity2.Data", "data":data})
        this.startActivity(p1,p2);
    }

    var Uri = Java.use("android.net.Uri");
    Uri.parse.implementation = function(strUri){
        send("UriParse");
        send(strUri);
        return this.parse(strUri);
    }


//    var Webview = Java.use("android.webkit.WebView")
//        Webview.loadUrl.overload("java.lang.String").implementation = function(url) {
//        send("[+]Loading URL from", url);
//        this.loadUrl.overload("java.lang.String").call(this, url);
//    }

    var WebView = Java.use("android.webkit.WebView");
    if (WebView != undefined){
        send("loadUrl");
        WebView.loadUrl.overload("java.lang.String").implementation = function(arg) {
        send(arg);
//        send({"type":"WebView", "data":arg})
        this.loadUrl(arg);
       }
    }


    var Window = Java.use("android.view.Window");
    var WindowManager = Java.use("android.view.WindowManager");
    Window.setFlags.implementation = function(flags, mask){
        send("WindowManagerSetflags");
        // 将 FLAG_SECURE 参数更改为 0
//        var newFlags = flags & ~WindowManager.LayoutParams.FLAG_SECURE;
        //var flag_secure = 8192
        var newFlags = flags & ~mask;
        // 调用原始方法
        this.setFlags(newFlags, mask);
    }



//
//    Java.choose('android.webkit.WebView',{
//        onMatch: function (instance) {
//            console.log("Found instance: " + instance);
//            console.log("URL: "+instance.getUrl());
//        },
//        onComplete: function () {
//            console.log('Finished')
//        }
//    });

});


//console.log("Script loaded successfully ");
//
//function callSecretFun() { //定义导出函数
//    Java.perform(function () { //找到隐藏函数并且调用
//        Java.choose("android.content.Intent", {
//            onMatch: function (instance) {
//                console.log("Found intent: " + instance);
//                console.log("Data: " + instance.getData());
//                console.log("Extras: " + instance.getExtras())
//                console.log("\n")
//            },
//            onComplete: function () { }
//        });
//    });
//}
//rpc.exports = {
//    callsecretfunction: callSecretFun //把callSecretFun函数导出为callsecretfunction符号，导出名不可以有大写字母或者下划线
//};