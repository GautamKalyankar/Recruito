// *************ChatWidget Code ***************



if (document.getElementById("topnav")) {
    console.log("after login");
    var id=sessionStorage.getItem("userId").toLocaleUpperCase()
        console.log("This is User Id"+id);
    azureChatWidgetCode();
}

else {
var setEventUserId = setTimeout(function () {
    if (document.readyState === "complete") {
        callEventUserId();
    }
}, 500);

function callEventUserId() {
    clearInterval(setEventUserId);
    var txt = document.getElementsByName("User")[0];
    txt.onblur = function (e) {
        console.log("User id accessed on blur");
        if (e.target.value) {
            sessionStorage.setItem("userId", e.target.value);
            sessionStorage.setItem("username",e.target.value);
        }
    };
    if (sessionStorage.getItem("userId") == null) {
        txt.onselect = function (e) {
            console.log("User id accessed on select");
            if (e.target.value) {
                sessionStorage.setItem("userId", e.target.value);
                sessionStorage.setItem("username",e.target.value);
            }
        };
    }
}
   


}

console.log("In Azure CW Code");

function azureChatWidgetCode() {

    console.log("in chat Widget");
    getTextforChatbot(
        window.location.origin +
          "/jde/E1Menu_About.mafService?e1.state=maximized&e1.mode=view&e1.namespace=&e1.service=E1Menu_About&RENDER_MAFLET=E1Menu"
      );

    async function getTextforChatbot(file) {
        let myObject = await fetch(file);
        let myText = await myObject.text();
        var parser = new DOMParser();
        var doc = parser.parseFromString(myText, "text/html");
        var jdeEnvForChatbot;
   
        let tableElements = doc.querySelectorAll("tr > td:last-child");
        var count = 0;
        for (let value of tableElements) {
          if (count == 5) {
            jdeEnvForChatbot = await value.innerHTML;
            console.log("this is jde Environment", jdeEnvForChatbot);
            sessionStorage.setItem("jdeenvir", jdeEnvForChatbot);
            break;
          } else {
            count++;
          }
        }
      }

     
    var div = document.createElement('div');
    div.setAttribute('id', 'lexChatwidget');
    document.body.appendChild(div);

    //IE
    (function (arr) {
        arr.forEach(function (item) {
            if (item.hasOwnProperty('remove')) { return; }
            Object.defineProperty(item, 'remove', { configurable: true, enumerable: true, writable: true, value: function remove() { this.parentNode.removeChild(this); } });
        });
    })([Element.prototype, CharacterData.prototype, DocumentType.prototype]);

    //npm build code below

}