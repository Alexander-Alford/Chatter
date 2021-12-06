import { Component } from '@angular/core';



@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
})


export class SignInComponent {

  public usernameSubmit: string | null = null;
  public passwordSubmit: string | null = null;
  public selectorSubmit: "MAKE" | "LOG" = "MAKE";

  public async manageUser(user: string|null, pass: string|null, selector: "MAKE" | "LOG" ){
  
    const sendObj: Object = {
      Username: user,
      Password: pass,
      Selector: selector
    };

    fetch("/api", 
    {
      method: 'POST',
      body: JSON.stringify(sendObj),
      headers: {'Content-Type': 'application/json; charset=UTF-8'} 
    })
    .then((response) => response.json())
    .then((sendObj) => { console.log('This is a test: ', sendObj); })
    .catch((error) => { console.log('Error: ', error); });
}

}
