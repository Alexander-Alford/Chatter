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


  public clientChatObject: Chat = {
    isChatting: false,
    secondChatter: null,
    chatterList: [],
    chattersOnline: 0,
    messageList: []
  };  


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


  async getChatterList(){

    const request: Object = {
      Selector: "CHATTERLIST"
    };

    let response: any = null;

    await fetch("http://127.0.0.1:500/api/chatroom")
    .then((response) => response.json())
    .then((data) => response = data)
  
  
    this.clientChatObject.chatterList = response.data;
  }

  ngOnInit(): void {
    this.getChatterList();
  }

}



