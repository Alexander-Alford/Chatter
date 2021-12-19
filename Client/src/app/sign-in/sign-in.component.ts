import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html'
})



export class SignInComponent implements OnInit{

  public usernameSubmit: string | null = "";
  public passwordSubmit: string | null = "";
  public isLoggedIn: boolean = false;
  public APIresultMessage: string | null = null;
  public lastAPIresult: "success" | "failure" | null = null;


  public setUsername(event: any){
    this.usernameSubmit = event.target.value;
  }
  public setPassword(event: any){
    this.passwordSubmit = event.target.value;
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
      this.isLoggedIn = true;
      this.usernameSubmit = res.data;
      return true;
    }
    else{
      this.isLoggedIn = false;
      return false;
    }
  }

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
        this.isLoggedIn = true;
      }
    }
    
    (responseJSON!.result === "success") ? (this.lastAPIresult = 'success') : (this.lastAPIresult = 'failure')

    this.APIresultMessage = responseJSON!.detail;
  }

  public async deleteUser(user: string|null, credential: string|null, selector: "DELETE"|"LOGOUT"){

    const request: Object = {
      Username: user,
      SessToken: credential,
      Selector: selector
    };

    let responseJSON: {result: string, detail: string} | null = null;

    await fetch("http://127.0.0.1:500/api/signin", 
    {
      method: 'DELETE',
      body: JSON.stringify(request),
      headers: {'Content-Type': 'application/json; charset=UTF-8'} 
    })
    .then((response) => response.json())
    .then((data) => responseJSON = data)
    //.then((sendObj) => { console.log('This is a test: ', sendObj); })
    //.catch((error) => { console.log('Error: ', error); });
    if(responseJSON!.result === "success"){
      document.cookie = "SessToken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
      this.isLoggedIn = false;
      this.usernameSubmit = "";
    }
    
    (responseJSON!.result === "success") ? (this.lastAPIresult = 'success') : (this.lastAPIresult = 'failure')
    
    this.APIresultMessage = responseJSON!.detail;
  }

 
  ngOnInit(): void {
    this.checkIfAuthIsGood();
  }

}
