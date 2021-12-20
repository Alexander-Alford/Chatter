import { Component, OnInit } from '@angular/core';
//import { SignInComponent } from '../sign-in/sign-in.component';


type Chatter = {
  inChat: string;
  primColor: string;
  secColor: string;
  name: string;
}

type Message = {
  author: string;
  content: string;
  time: number;
}

type Chat = {
  selfUsername: string | null;
  isChatting: boolean;
  secondChatter: Chatter | null;
  chatterList: Chatter[];
  chattersOnline: number;
  messageList: Message[];
};


@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
})
export class ChatComponent implements OnInit {

  public primaryColorBuf: string = "#000000";
  public secondaryColorBuf: string = "#FFFFFF";


  public clientChatObject: Chat = {
    selfUsername: null,
    isChatting: false,
    secondChatter: null,
    chatterList: [],
    chattersOnline: 0,
    messageList: []
  };  

  public setPriCol(col: string){
    console.log(this.primaryColorBuf)
    this.primaryColorBuf = col;
    console.log(this.primaryColorBuf)
  }

  public setSecCol(col: string){
    this.secondaryColorBuf = col;
  }

  public getCookie(name: string|null) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      const buf = parts.pop()!.split(';').shift()
      console.log(buf)
      if (buf === undefined){
        return null;
      }
      else{
        return buf;
      }
    }
    else {
      return null;
    }
  }

  public async checkIfAuthIsGood(){

    let filteredtoken = this.getCookie("SessToken");
    if(filteredtoken === null || filteredtoken === ""){
      filteredtoken = "0";
    }

    let res: any;

    await fetch("http://127.0.0.1:500/api/authcheck/" + filteredtoken)
    .then((response) => response.json())
    .then((data) => res = data)

    if(res.result === "success"){
      this.clientChatObject.selfUsername = res.data;
      return true;
    }
    else{
      return false;
    }
  }

  public async getChatterList(){

    const request: Object = {
      Selector: "CHATTERLIST"
    };

    let response: any = null;

    await fetch("http://127.0.0.1:500/api/chatroom")
    .then((response) => response.json())
    .then((data) => response = data)
  
  
    this.clientChatObject.chatterList = response.data;
    this.clientChatObject.chattersOnline = this.clientChatObject.chatterList.length;
  }

  public async getColors(){

    let filteredtoken = this.getCookie("SessToken");
    if(filteredtoken === null || filteredtoken === ""){
      filteredtoken = "0";
    }

    let res: any;

    await fetch("http://127.0.0.1:500/api/color/" + filteredtoken)
    .then((response) => response.json())
    .then((data) => res = data)

    if(res.result == "success"){
      let pc = <HTMLInputElement>document.getElementById("prim-color");
      let sc = <HTMLInputElement>document.getElementById("sec-color");
      pc.value = res.pCol;
      sc.value = res.sCol;
    }

    
  }

  public async setColors(pri: string, sec: string){

    const reqObj: Object = {
        SessToken: this.getCookie("SessToken"),
        PrimaryColor: pri,
        SecondaryColor: sec
    }

    let response: any = null;

    await fetch("http://127.0.0.1:500/api/account", 
    {
      method: 'PATCH',
      body: JSON.stringify(reqObj),
      headers: {'Content-Type': 'application/json; charset=UTF-8'} 
    })
    .then((response) => response.json())
    .then((data) => response = data)



  }

  ngOnInit(): void {
    this.checkIfAuthIsGood();
    this.getChatterList();
    this.getColors();
  }

}



