<template>
  <div :style="{ background: backgroundColor }">
    <beautiful-chat
      :alwaysScrollToBottom="alwaysScrollToBottom"
      :close="closeChat"
      :colors="colors"
      :clearText="clearText"
      :isOpen="isChatOpen"
      :messageList="messageList"
      :messageStyling="messageStyling"
      :newMessagesCount="newMessagesCount"
      :onMessageWasSent="onMessageWasSent"
      :open="openChat"
      :participants="participants"
      :showCloseButton="true"
      :showLauncher="true"
      :showEmoji="false"
      :showFile="true"
      :showLoginForm="showLoginForm"
      :chartLabel="chartLabel"
      :chartData="chartData"
      :submitLogin="submitLogin"
      :userId="userId"
      :showTypingIndicator="showTypingIndicator"
      :titleImageUrl="titleImageUrl"
      @onType="handleOnType"
      @edit="editMessage"
      @remove="removeMessage"
    >
    </beautiful-chat>
  </div>
</template>

<script>
import chatParticipants from "./chatProfiles";
import availableColors from "./colors";

var tempMessage,tempFlag=0,file_message,chatInitialized=false;
var flaskURL="http://localhost:5000/post",userType="hi applicant";
export default {
  name: "app",
  components: {},
  data() {
    return {
      participants: chatParticipants,
      titleImageUrl:
        "https://jde-videos.herokuapp.com/images/liz.png",
      messageList: [],
      newMessagesCount: 0,
      isChatOpen: false,
      showTypingIndicator: "",
      colors: null,
      availableColors,
      chosenColor: null,
      alwaysScrollToBottom: true,
      messageStyling: true,
      userIsTyping: false,
      showLoginForm: false,
      chartLabel: [],
      chartData: [],
      userId: "",
    };
  },
  created() {
    this.setColor("nyna");
  },
  methods: {
    sendMessage(botReply) {
      const text=botReply.respMessage
      //const text = botReply.data.text;
      let showchart=false;
    
      let chartMessage =  botReply.attachment;
      console.log(botReply)
      if(chartMessage && !botReply.suggestion) {
        let chartArr = [];
        var arr=chartMessage.chartLabel
        for (let i = 0; i < arr.length; i++) {
          chartArr.push(arr[i].split(" "));
        }
        this.chartLabel = chartArr;
        this.chartData = chartMessage.chartData;
        showchart=true;
      } 
      else {
        showchart=false;
      }
      console.log(text)
      if (text.length > 0) {
        this.newMessagesCount = this.isChatOpen
          ? this.newMessagesCount
          : this.newMessagesCount + 1;
      //this.onMessageFromBot(text)
        if (text.split("^").length > 1) {
            
            if(chartMessage){
              this.sendPlainTextToUser(text.split("^")[0],[],chartMessage);
            }
            else{
              this.sendPlainTextToUser(text.split("^")[0]);
            }
            if(botReply.suggestion){
              this.sendPlainTextToUser(text.split("^")[1],botReply.suggestion)
            }
            else{
              this.sendPlainTextToUser(text.split("^")[1]);
            }
        }
        else if(botReply.toself){
          this.onMessageFromBot({
            author: "botReply.author",
            type: "text",
            id: "botReply.id",
            data: { text },
            imageUrl: "",
            videoUrl: "",
            showchart: showchart
          });
          fetch(flaskURL, {
          method:"POST",
          headers: {
            "Content-Type":"application/json; charset=UTF-8"
          },
          body: JSON.stringify({message : "Done Matching"})
          })
          .then (resp => resp.json())
          .then (data => {
            console.log(data);
            this.sendMessage(data)
          }) 
          .catch(error =>{
            console.log(JSON.stringify({message : message.data.text}))
            console.log(error);
          })
        }
        else if (botReply.suggestion) {
          this.onMessageFromBot({
            author: "botReply.author",
            type: "text",
            id: "botReply.id",
            data: { text },
            suggestions: botReply.suggestion,
            messageType: botReply.messageType,
            imageUrl: "",
            videoUrl: "",
            showchart: showchart
          });
        } else {
          this.onMessageFromBot({
            author: "botReply.author",
            type: "text",
            id: "botReply.id",
            data: { text },
            imageUrl: "",
            videoUrl: "",
            showchart: showchart
          });
        }
       }
    },
    handleTyping(text) {
      this.showTypingIndicator =
        text.length > 0
          ? this.participants[this.participants.length - 1].id
          : "";
    },
    onMessageFromBot(message) {
      this.chosenColor;
      this.colors.receivedMessage;
      this.messageStyling;
      this.messageList = [
        ...this.messageList,
        Object.assign({}, message, { id: message.id }),
      ];

      // if (sessionStorage.getItem("authToken")) {
      //   this.showLoginForm = false;
      // } else {
      //   this.showLoginForm = true;
      // }
      // if (message.showGlobalAction == true) {
      //   this.showGlobalAction = true;
      // } else {
      //   this.showGlobalAction = false;
      // }
    },
    onMessageWasSent(message) {
      this.chosenColor, this.colors.sentMessage;
      this.messageStyling;
      const _this = this;
      var messageUserId;

      console.log(message);
      
      // if(message.data.text=="hi applicant")
      // {
      //   tempMessage=message;
      //   console.log(tempMessage);
      // }
      if(message.type=="file")
      {
        if(tempFlag==0){
          tempMessage={
            author:"me",
            type: "text",
            data:{"text":"Uploading Resume..."}
          }
          //tempMessage.data.text="Uploading Resume...";
          file_message=message
          this.tempfunction(tempMessage,file_message);
          
        }
        const formData  = new FormData();

        for(const name in message.data) {
          formData.append(name, message.data[name]);
        }

        fetch('http://localhost:5000/postresume', {
          method:"POST",
          // headers: {
          //   "Content-Type": ""
          // },
          body: formData
        })
        .then (resp => resp.json())
        .then (data => {
          console.log(data);
          this.sendMessage(data)
        }) 
        .catch(error =>{
          console.log(JSON.stringify({message : message.data.text}))
          console.log(error);
        })
      }
      else {
      if(message.data.text!="Uploading Resume..."){
          fetch(flaskURL, {
            method:"POST",
            headers: {
              "Content-Type":"application/json; charset=UTF-8"
            },
            body: JSON.stringify({message : message.data.text})
          })
          .then (resp => resp.json())
          .then (data => {
            console.log(data);
            this.sendMessage(data)
          }) 
          .catch(error =>{
            console.log(JSON.stringify({message : message.data.text}))
            console.log(error);
          })
      }
      else{
        tempFlag=1;
      }
      
      }


      if (sessionStorage.getItem("authToken")) {
        this.showLoginForm = false;
      }

      let messageToBot;
      if (Object.prototype.hasOwnProperty.call(message.data.text, "label")) {
        if (message.data.text.value.includes("https")) {
          window.open(message.data.text.value, "_blank");
          return;
        }
      }
      if (Object.prototype.hasOwnProperty.call(message.data.text, "label")) {
        messageToBot = message.data.text.value;
        message.data.text = message.data.text.label;
      }
      if (message.author !== "hidden") {
        this.messageList = [
          ...this.messageList,
          Object.assign({}, message, { id: this.userId }),
        ];
        messageUserId = this.$store.state.userId;
      } else {
        messageUserId = message.id;
      }
      if (messageToBot === undefined) {
        messageToBot = message.data.text;
        this.$store.state.firstInput = messageToBot;
      }
      // //Post activities to the bot:
      // // if (sessionStorage.getItem("authToken")) {
      //   directLine
      //     .postActivity({
      //       from: {
      //         id: messageUserId,
      //         name: sessionStorage.getItem("username"),
      //         jdeenv:sessionStorage.getItem("jdeenvir")
            
      //       }, // required (from.name is optional)
      //       type: "message",
      //       text: messageToBot,
      //     })
      //     .subscribe(
      //       (id) => console.log("Posted activity, assigned ID ", id),
      //       (error) => console.log("Error posting activity", error)
      //     );
      // // } else {
      // //   this.showLoginForm = true;
      // // }

      // //Listen to activities sent from the bot:
      // directLine.activity$
      //   .filter(
      //     (activity) =>
      //       activity.type === "message" && activity.from.id === config.BotName
      //   )
      //   .subscribe(function (messageFromBot) {
      //     // if (messageFromBot.type === "message") {
      //     let text = messageFromBot.text;
      //     let id = messageFromBot.from.id;
      //     let messageId = _this.$store.state.messageId;
      //     let imageUrl = "";
      //     let videoUrl = "";
      //     let responseCard = messageFromBot.attachments;
      //     let quickActions = messageFromBot.suggestedActions;
      //     // let list = messageFromBot.attachmentLayout

      //     // if (!messageFromBot.recipient) {
      //     if (messageId !== messageFromBot.id) {
      //       _this.$store.state.messageId = messageFromBot.id;
      //       console.log("received activity ", messageFromBot);

      //       if (responseCard) {
      //         if (responseCard[0].contentType === "application/pdf") {
      //           _this.sendListToUser(
      //             messageFromBot.text,
      //             messageFromBot.attachments,
      //             id,
      //             imageUrl,
      //             ""
      //           );
      //         } else if (
      //           responseCard[0].contentType ===
      //           "application/vnd.microsoft.card.adaptive"
      //         ) {
      //           _this.sendListToUser(
      //             messageFromBot.text,
      //             messageFromBot.attachments[0].content,
      //             id,
      //             imageUrl,
      //             "carousel"
      //           );
      //         } else if (
      //           responseCard[0].contentType ===
      //           "application/vnd.microsoft.card.video"
      //         ) {
      //           videoUrl = responseCard[0].content.media[0].url;
      //           let text = responseCard[0].content.title;
      //           _this.sendPlainTextToUser(text, id, "", videoUrl);
      //         } else {
      //           _this.sendListToUser(
      //             messageFromBot.attachments[0].content.text,
      //             messageFromBot.attachments[0].content.buttons,
      //             id,
      //             imageUrl,
      //             ""
      //           );
      //         }
      //       } else if (quickActions) {
      //         _this.sendListToUser(
      //           messageFromBot.text,
      //           quickActions.actions,
      //           id,
      //           imageUrl,
      //           "global-action"
      //         );
      //       } else {
      //         _this.sendPlainTextToUser(text, id, imageUrl, videoUrl);
      //       }
      //     }
      //     if (text === "Invalid token! Please re-enter your password again.") {
      //       // this.deleteAndInitMessage();
      //       //sessionStorage.removeItem("authToken");
      //       // this.showLoginForm = true;
      //     }
      //     //   }
      //     // }
      //   });
    },
    tempfunction(tempMessage,file_message){
      tempFlag=1;
      this.onMessageWasSent(tempMessage);
      // this.onMessageWasSent(file_message);
    },
    getMenuList(menuArray) {
      var listMenu = [];
      if (menuArray[0].contentType === "application/pdf") {
        menuArray.forEach(function (menu) {
          listMenu.push({
            label: menu.name,
            value: menu.contentUrl,
          });
        });
      } else if (
        menuArray[0].contentType === "application/vnd.microsoft.card.adaptive"
      ) {
        menuArray.forEach(function (menu) {
          // console.log(menu)
          listMenu.push({
            label: menu.content.title,
            value: menu.content.description,
          });
        });
      } else {
        menuArray.forEach(function (menu) {
          listMenu.push({
            label: menu.title,
            value: menu.value,
          });
        });
      }

      return listMenu;
    },
     sendMessageOnOpen(){
      let person;
      if(window.location.pathname.split('/')[1]=="recruiter"){
        person = "recruiter"
        flaskURL="http://localhost:5000/post2recruiter"
      }else{
        person = "applicant"
        flaskURL="http://localhost:5000/post"
      }
      this.onMessageWasSent({
        author: "hidden",
        type: "text",
        id: "hidden",
        data: {
          text: "hi " + person,
        },
      });
    },
    openChat() {
      this.isChatOpen = true;
      this.newMessagesCount = 0;
      if(chatInitialized==false){
            this.sendMessageOnOpen();
      //   var hiddenMessage={
      //       author:"hidden",
      //       type: "text",
      //       data:{"text":userType}
      // }
      //   this.onMessageWasSent(hiddenMessage)
      }
      chatInitialized=true;
      
      // this.deleteAndInitMessage();
    },
    closeChat() {
      this.isChatOpen = false;
    },
    clearText() {
      console.log("clear clicked");
      const _this = this;
      this.$store.state.clickedRefresh = true;
      setTimeout(function () {
        _this.$store.state.messageReceived = true;
      }, 600);
      this.deleteAndInitMessage();
      this.sendMessageAfterRefresh();

    },
    submitLogin() {
      console.log("hello from chatbot")
      // alert('hello')
      // this.callLoginService();
      // sessionStorage.setItem('authToken', 'abc123')
      // this.deleteAndInitMessage();
    },
    // callLoginService() {
    //   // console.log(this.$store.state.firstInput);
    //   let jsonInput = {
    //     username: this.userId,
    //     password: document.getElementById("password").value,
    //   };

    //   axios({
    //     method: "POST",
    //     url: "http://130.61.54.223/FetchAuthenticationTokenFromNOW",
    //     data: jsonInput,
    //     headers: { "content-type": "application/json" },
    //   }).then(
    //     (result) => {
    //       console.log(result.data);
    //       if (result.data.status === "SUCCESS") {
    //         var token = result.data.tokenvalue;
    //         sessionStorage.setItem("authToken", token);
    //         this.onMessageWasSent({
    //           author: "me",
    //           type: "text",
    //           id: "me",
    //           data: {
    //             text: this.$store.state.firstInput,
    //           },
    //         });
    //       } else if (result.data.status === "ERROR") {
    //         var msg;
    //         if (result.data.tokenvalue === "Invalid Credentials") {
    //           msg = "You have entered a wrong password. Please enter again";
    //         } else {
    //           msg = "Something went wrong! Please try again later.";
    //         }
    //         this.onMessageFromBot({
    //           author: "Nyna",
    //           type: "text",
    //           id: "Nyna",
    //           data: {
    //             text: msg,
    //           },
    //         });
    //         this.showLoginForm = true;
    //       } else {
    //         this.onMessageFromBot({
    //           author: "Nyna",
    //           type: "text",
    //           id: "Nyna",
    //           data: {
    //             text: "You have entered a wrong password. Please enter again",
    //           },
    //         });
    //         this.showLoginForm = true;
    //       }
    //     },
    //     (error) => {
    //       this.showLoginForm = true;
    //       console.error(error);
    //     }
    //   );
    // },
    deleteAndInitMessage() {
      var allMessageList = "sc-message-list";
      var messagesData = "sc-messages";
      let messageCount = "";
      var i = "";
      let j = "";
      var messageLists = document.getElementsByClassName(allMessageList);
      var messages = messageLists[0].getElementsByClassName(messagesData);
      if (messages.length >= 1) {
        for (i = 0; i < messages.length; i++) {
          messageCount = messages[i].childElementCount;
          for (j = 0; j < messageCount; j++) {
            if (
              document.querySelectorAll("#sc-message-id")[0].style.cssText !=
              "display: none;"
            ) {
              document.querySelectorAll("#sc-message-id")[0].innerHTML = "";
              document.querySelectorAll("#sc-message-id")[0].remove();
            }
          }
        }
      }
      // this.$store.state.userId = this.createUserId();
      this.$store.state.sessionAttributes = {};
      // this.showLoginForm = false;
      // this.sendMessageAfterRefresh();
     
    },
    sendMessageAfterRefresh() {
      this.onMessageWasSent({
        author: "hidden",
        type: "text",
        id: "hidden",
        data: {
          text: "Refresh",
        },
      });
    },
    sendConfirmation(message) {
      this.onMessageWasSent({
        author: "hidden",
        type: "text",
        id: "hidden",
        data: {
          text: "Confirm",
        },
        sessionAttributes: message.sessionAttributes,
      });
    },
    sendPlainTextToUser(text,suggestions=[],chartMessage={}) {
      if(Object.keys(chartMessage).length!=0){
        this.sendMessage({
          respMessage:text,
          attachment: chartMessage
        });
      }
      else if(suggestions.length==0){
        this.sendMessage({
          respMessage:text,
        });
      }
      else
      {
        this.sendMessage({
          respMessage:text,
          suggestion:suggestions
        });
      }
    },
    sendListToUser(text, responseCard, id, imageUrl, messageType) {
      this.sendMessage({
        author: chatParticipants[0].id,
        type: "text",
        id: id,
        data: { text },
        suggestion: this.getMenuList(responseCard),
        messageType: messageType,
        imageUrl: imageUrl,
      });
    },
    setColor(color) {
      this.colors = this.availableColors[color];
      this.chosenColor = color;
    },
    showStylingInfo() {
      this.$modal.show("dialog", {
        title: "Info",
        text:
          "You can use *word* to <strong>boldify</strong>, /word/ to <em>emphasize</em>, _word_ to <u>underline</u>, `code` to <code>write = code;</code>, ~this~ to <del>delete</del> and ^sup^ or ¡sub¡ to write <sup>sup</sup> and <sub>sub</sub>",
      });
    },
    messageStylingToggled(e) {
      this.messageStyling = e.target.checked;
    },
    handleOnType() {
      this.$root.$emit("onType");
      this.userIsTyping = true;
    },
    editMessage(message) {
      const m = this.messageList.find(function (m) {
        m.id === message.id;
      });
      m.isEdited = true;
      m.data.text = message.data.text;
    },
    removeMessage(message) {
      if (confirm("Delete?")) {
        const m = this.messageList.find(function (m) {
          m.id === message.id;
        });
        m.type = "system";
        m.data.text = "This message has been removed";
      }
    },
    like(id) {
      const m = this.messageList.findIndex(function (m) {
        m.id === id;
      });
      var msg = this.messageList[m];
      msg.liked = !msg.liked;
      this.$set(this.messageList, m, msg);
    },
    createUserId() {
      return Math.random()
        .toString(36)
        .replace(/[^a-z]+/g, "")
        .substr(0, 5);
    },
    removeElement(elms) {
      elms[0].childNodes.forEach(function (elm) {
        elm.remove();
      });
    },
    getUserName() {
      var username = document.getElementById("usernameDiv").innerText;
      sessionStorage.setItem("username", username);
    },
  },

  computed: {
    linkColor() {
      return this.chosenColor === "dark"
        ? this.colors.sentMessage.text
        : this.colors.launcher.bg;
    },
    backgroundColor() {
      return this.chosenColor === "dark" ? this.colors.messageList.bg : "#fff";
    },
  },
  async mounted() {
    // this.getUserName();
    this.$store.state.userId = sessionStorage.getItem("userId");
    this.userId = this.$store.state.userId;
    this.messageList.forEach(function (x) {
      x.liked = false;
    });
  },
  beforeMount() {
    console.log("set userID");
    sessionStorage.setItem("userId", "Saurav");
    sessionStorage.setItem("username","Saurav");
    sessionStorage.setItem("jdeenvir","JQATHA");

  },
};
</script>

<style>
.messageStyling {
  font-size: normal;
}

.sc-user-input--buttons {
  right: 0px !important;
  top: 5px;
}

p {
  margin-top: 0 !important;
  line-height: 1.4 !important;
  /* color: rgb(0, 0, 0) ; */
}

.sc-message--text-content {
  margin-bottom: 6px !important;
}
</style>
