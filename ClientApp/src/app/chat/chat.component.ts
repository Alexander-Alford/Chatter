import { Component } from '@angular/core';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
})
export class ChatComponent {

  user: object = {};  

}



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
  secondChatter: Chatter;
  chatterList: Chatter[];
  chattersOnline: number;
}