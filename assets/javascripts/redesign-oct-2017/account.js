
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
  var b = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return b ? b.pop() : '';
}

function addListItem (text, href, listItemClass, linkClass) {
  var listItem = createEl('li');
  listItem.className = listItemClass;
  var anchor = createEl('a');
  anchor.href = href;
  anchor.className = linkClass;
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
  addListItem ('Register', ukdit.config.urls.register, 'anonymous', 'register');
}

function addSignIn () {
  addListItem ('Sign in', ukdit.config.urls.signin, 'anonymous', 'signin');
}

function addProfile () {
  addListItem ('Profile', ukdit.config.urls.profile, 'authenticated', '');
}

function addSignOut () {
  addListItem ('Sign out', ukdit.config.urls.signout, 'authenticated', 'signout');
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