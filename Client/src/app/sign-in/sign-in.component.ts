import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html'
})


export class SignInComponent{

  public usernameSubmit: string | null = "TEST";
  public passwordSubmit: string | null = "1234";
  public isLoggedIn: boolean = false;



  public async postUser(user: string|null, pass: string|null, selector: "MAKE"|"LOGIN"){
  
    const request: Object = {
      Username: user,
      Password: pass,
      Selector: selector
    };

    let responseJSON: {result: string, detail: string} | null = null;

    await fetch("http://127.0.0.1:500/api/signin", 
    {
      method: 'POST',
      body: JSON.stringify(request),
      headers: {'Content-Type': 'application/json; charset=UTF-8'} 
    })
    .then((response) => response.json())
    .then((data) => responseJSON = data)

    if(selector === "LOGIN"){
      if(responseJSON!.result === "success")
      {
        document.cookie = "SessToken=" + responseJSON!.detail + "; path=/"
      }
    }
      

  }

  public async deleteUser(user: string|null, credential: string|null, selector: "DELETE"|"LOGOUT"){
  
    const request: Object = {
      Username: user,
      SessToken: credential,
      Selector: selector
    };

    let responseJSON: {result: string, detail: string} | null = null;

    fetch("http://127.0.0.1:500/api/signin", 
    {
      method: 'DELETE',
      body: JSON.stringify(request),
      headers: {'Content-Type': 'application/json; charset=UTF-8'} 
    })
    .then((response) => response.json())
    //.then((sendObj) => { console.log('This is a test: ', sendObj); })
    //.catch((error) => { console.log('Error: ', error); });
    if(responseJSON!.result === "success"){
      document.cookie = "SessToken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
    }
  }

  //public createSessionCookie(inputToken: string|null){
  //  document.cookie = "SessToken=" + inputToken
  //}


}
