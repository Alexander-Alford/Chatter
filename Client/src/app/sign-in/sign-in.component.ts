import { Component } from '@angular/core';



@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
})


export class SignInComponent {

  public usernameSubmit: string | null = null;
  public passwordSubmit: string | null = null;
  public isLoggedIn: boolean = false;

  public async postUser(user: string|null, pass: string|null, selector: "MAKE"|"LOGIN"){
  
    const request: Object = {
      Username: user,
      Password: pass,
      Selector: selector
    };

    fetch("http://127.0.0.1:500/api/signin", 
    {
      method: 'POST',
      body: JSON.stringify(request),
      headers: {'Content-Type': 'application/json; charset=UTF-8'} 
    })
    .then((response) => response.json())
    .then((sendObj) => { console.log('This is a test: ', sendObj); })
    .catch((error) => { console.log('Error: ', error); });
  }

  public async deleteUser(credential: string|null, selector: "DELETE"|"LOGOUT"){
  
    const request: Object = {
      SessToken: credential,
      Selector: selector
    };

    fetch("/api", 
    {
      method: 'DELETE',
      body: JSON.stringify(request),
      headers: {'Content-Type': 'application/json; charset=UTF-8'} 
    })
    .then((response) => response.json())
    .then((sendObj) => { console.log('This is a test: ', sendObj); })
    .catch((error) => { console.log('Error: ', error); });
  }

}
