import { Component } from '@angular/core';



type Chatter = {
  id: number;
  color: string;
  name: string;
}

type Message = {
  content: string;
  time: number;
}

type Chat = {
  isChatting: boolean;
  secondChatter: Chatter | null;
  chatterList: Chatter[];
  chattersOnline: number;
  messageList: Message[];
} | null;


@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
})
export class ChatComponent {


  public clientChatObject: Chat = {
    isChatting: true,
    secondChatter: null,
    chatterList: [],
    chattersOnline: 0,
    messageList: []
  };  

}



