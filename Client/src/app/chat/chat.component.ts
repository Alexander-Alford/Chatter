import { Component } from '@angular/core';
//import { SignInComponent } from '../sign-in/sign-in.component';


type Chatter = {
  sessionToken: string;
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
export class ChatComponent {


  public clientChatObject: Chat = {
    isChatting: false,
    secondChatter: null,
    chatterList: [],
    chattersOnline: 0,
    messageList: []
  };  

}



