
(function (ukdit) {
  var ssoCookieName = "sso_display_logged_in";
  var list = null;

function createEl(el, target){
  var ne = document.createElement(el);
  if( target )
    target.appendChild(ne);
  return ne;
 }

function createText(content, target){
  var ne = document.createTextNode(content);
  target.appendChild(ne);
  return ne;
}

function readCookie(name) {
  var cookies = {};
  if(cookies){ return cookies[name]; }

  var c = document.cookie.split('; ');

  for(var i=c.length-1; i>=0; i--){
    var C = c[i].split('=');
    cookies[C[0]] = C[1];
  }

  return cookies[name];
}

function addListItem (text, href, className) {
  var listItem = createEl('li');
  listItem.className = className;
  var anchor = createEl('a');
  anchor.href = href;
  anchor.className = className;
  createText(text, anchor);
  listItem.appendChild(anchor);
  list.appendChild(listItem);
}

function setLoggedIn () {
  addProfile();
  addSignOut();
}

function setLoggedOut () {
  addRegister();
  addSignIn();
}

function addRegister () {
  addListItem ('Register', ukdit.config.urls.register, 'anonymous');
}

function addSignIn () {
  addListItem ('Login', ukdit.config.urls.signin, 'anonymous signin');
}

function addProfile () {
  addListItem ('Profile', ukdit.config.urls.profile, 'profile');
}

function addSignOut () {
  addListItem ('Sign out', ukdit.config.urls.signout, 'signout');
}

function empty() {
  while (list.firstChild) {
    list.removeChild(list.firstChild);
  }
}

function setLoginStatus() {
  var cookieValue = readCookie(ssoCookieName);
  if (cookieValue == 'true') {
    setLoggedIn();
  } else {
    setLoggedOut();
  }
}

function init () {
  list = document.getElementsByClassName('account-links')[0];
  if (list) {
    empty();
    setLoginStatus();
  }
}

init();

})(window.ukdit);