// import config from './config.js';

// The current server ip address.

// let server_ip = "https://bayanfatwa.site"
let server_ip = "http://127.0.0.1:8000"


// The default list of guest websites.
var guest_sites = [
    "https://www.islamweb.net",
    "https://islamqa.info",
    "https://binbaz.org.sa",
    "https://dorar.net",
    "https://islamarchive.cc",
    "https://al-maktaba.org"
]

// To indicate whether the current session is a guest session.
var is_guest = true

// Global user information that is populated when a user is signed in.
var global_name = ""
var global_email = ""
var global_password = ""

var global_sites = [
    "https://www.islamweb.net",
    "https://islamqa.info",
    "https://binbaz.org.sa",
    "https://dorar.net",
    "https://islamarchive.cc",
    "https://al-maktaba.org"
]

var default_sites = [...global_sites]

var draft_sites = []

var searchHistory = []
var savedAnswers = []

var isMobile = false; //initiate as false

// device detection
if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent) 
    || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) { 
    isMobile = true;
}

var snippet_length = isMobile ? 75 : 500

var current_query = ''

var default_answer_extraction = true
var default_bert_reranking = false
var default_is_specific = true

var default_verses_extraction = true
var default_hadith_extraction = true

var verses_extraction = default_verses_extraction
var hadith_extraction = default_hadith_extraction

var local_verses_extraction_choice = default_verses_extraction
var local_hadith_extraction_choice = default_hadith_extraction

var answer_extraction = default_answer_extraction
var bert_reranking = default_bert_reranking
var is_specific = default_is_specific

start_time = ""
end_time = ""

auth_cookies = document.cookie
console.log("auth_cookies")
console.log(auth_cookies)

if (auth_cookies.length > "email=; password=".length) {
    auth_cookies_split = auth_cookies.split('; ')
    _email = auth_cookies_split[0].substring("email=".length, auth_cookies_split[0].length)
    _email = decodeURIComponent(_email)
    _password = auth_cookies_split[1].substring("password=".length, auth_cookies_split[1].length)
    _password = decodeURIComponent(_password)

    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === 4) {
            console.log(httpRequest.response)
            console.log(typeof (httpRequest.response))
            // If either information is incorrect, show alert.
            if (httpRequest.response == "Unauthorized Access") {
                setAuthCookies("","")
            } else {
                // Otherwise, sign in and update global information.
                response = JSON.parse(httpRequest.response)
                global_name = response['name']
                global_email = _email
                global_password = _password
                global_sites = response['sites']
                is_guest = false
                signInFrontendUpdate()
            }
        }
    }

    httpRequest.open('GET', `${server_ip}/validation`, true);
    httpRequest.withCredentials = true;
    httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${_email}:${_password}`));
    httpRequest.send();
}

if (!isMobile) {
    window.onmousemove = function (e) {
        var tooltipSpan = document.getElementsByClassName('tooltip-span');
        if (tooltipSpan.length > 0) {
            for (let i = 0; i < tooltipSpan.length; i++) {
                var x = e.clientX, y = e.clientY;
                tooltipSpan[i].style.top = (y) + 'px';
                tooltipSpan[i].style.left = (x) + 'px';
            }
        }
    };
} else {
    window.ontouchstart = function (e) {
        var tooltipSpan = document.getElementsByClassName('tooltip-span');
        if (tooltipSpan.length > 0) {
            for (let i = 0; i < tooltipSpan.length; i++) {
                var evt = (typeof e.originalEvent === 'undefined') ? e : e.originalEvent;
                var touch = evt.touches[0] || evt.changedTouches[0];
                // x = touch.pageX;
                // y = touch.pageY;
                x = touch.clientX;
                y = touch.clientY;
                // var x = e.clientX, y = e.clientY;
                tooltipSpan[i].style.top = (y+10) + 'px';
                tooltipSpan[i].style.left = (x+10) + 'px';
            }
        }
    }
    window.ontouchmove = function (e) {
        var tooltipSpan = document.getElementsByClassName('tooltip-span');
        if (tooltipSpan.length > 0) {
            for (let i = 0; i < tooltipSpan.length; i++) {
                var evt = (typeof e.originalEvent === 'undefined') ? e : e.originalEvent;
                var touch = evt.touches[0] || evt.changedTouches[0];
                x = touch.clientX;
                y = touch.clientY;
                tooltipSpan[i].style.top = (y+10) + 'px';
                tooltipSpan[i].style.left = (x+10) + 'px';
            }
        }
    }
}

/**
 * Switch between sign in and register tabs.
 * @param  {string} clickedBy The type of button that called the function.
 */
function switchSignInRegister(clickedBy) {
    if (clickedBy === 'signIn') {
        if (document.getElementById("registerTab").className == "nav-link active") {
            document.getElementById("signInTab").className = "nav-link active"
            document.getElementById("registerTab").className = "nav-link"
            showLoginForm()
        }
    } else if (clickedBy === 'register') {
        if (document.getElementById("signInTab").className == "nav-link active") {
            document.getElementById("registerTab").className = "nav-link active"
            document.getElementById("signInTab").className = "nav-link"
            showRegisterForm()
        }
    }
}

/**
 * Generate and show login form.
 */
function showLoginForm() {
    valForm = document.getElementById("valForm")
    console.log(valForm)
    valForm.innerHTML = `
    <div class="form-group row">
        <div class="col">
            <input type="email" class="form-control" id="inputEmail" placeholder="البريد الإلكتروني">
        </div>
    </div>
    <div class="form-group row">
        <div class="col">
            <input type="password" class="form-control" id="inputPassword" placeholder="الرمز السري">
        </div>
    </div>
    <div class="modal-footer">
        <button type="submit" class="btn btn-primary" onclick="signInValidation()" id="loginButton">تسجيل الدخول</button>
    </div>
    `
}

/**
 * Generate and show registration form.
 */
function showRegisterForm() {
    valForm = document.getElementById("valForm")
    console.log(valForm)
    valForm.innerHTML = `
    <div class="form-group row">
        <div class="col">
            <input type="text" class="form-control" id="inputName" placeholder="الاسم">
        </div>
    </div>
    <div class="form-group row">
        <div class="col">
            <input type="email" class="form-control" id="inputEmail" placeholder="البريد الإلكتروني">
        </div>
    </div>
    <div class="form-group row">
        <div class="col">
            <input type="password" class="form-control" id="inputPassword" placeholder="الرمز السري">
        </div>
    </div>
    <div class="form-group row">
        <div class="col">
            <input type="password" class="form-control" id="inputConfirmPassword" placeholder="تأكيد الرمز السري">
        </div>
    </div>
    <div class="modal-footer">
        <button type="submit" class="btn btn-primary" onclick="registerValidation()" id="registerButton">إنشاء حساب جديد</button>
    </div>
    `
}

/**
 * Validate registration information.
 */
function registerValidation() {
    inputName = document.getElementById('inputName').value.trim()
    inputEmail = document.getElementById('inputEmail').value.trim()
    inputPassword = document.getElementById('inputPassword').value
    inputConfirmPassword = document.getElementById('inputConfirmPassword').value

    // If name is empty, show appropriate alert and return.
    if (inputName == "") {
        showAlert('val', 'warning', 'لا يمكن ترك الاسم فارغا')
        return
    }

    // If email is empty, show appropriate alert and return.
    if (inputEmail == "") {
        showAlert('val', 'warning', 'لا يمكن ترك البريد الالكتروني فارغا')
        return
    }

    // If email is not an email, show appropriate alert and return.
    if (!validateEmail(inputEmail)) {
        showAlert('val', 'warning', 'صيغة البريد الاكتروني غير صحيحة')
        return
    }

    // If password is less than eight characters, show appropriate alert and return.
    if (inputPassword.length < 8) {
        showAlert('val', 'warning', 'كلمة السر يجب أن تكون من 8 خانات على الأقل')
        return
    }

    // If passwords don't match, show appropriate alert and return.
    if (inputPassword != inputConfirmPassword) {
        showAlert('val', 'warning', 'كلمة السر غير مطابقة')
        return
    }

    enableButton('register', 'light', false, 'إنشاء حساب جديد')
    register(inputName, inputEmail, inputPassword)
}

/**
 * Register an account.
 * @param  {string} name The user's name.
 * @param  {string} email The user's email.
 * @param  {string} password The user's password.
 */
function register(name, email, password) {

    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === 4) {
            console.log(httpRequest.response)
            console.log(typeof (httpRequest.response))

            response = JSON.parse(httpRequest.response)

            // If an account is registered, update global details.
            if (response['registration']) {
                global_name = name
                global_email = email
                global_password = password
                global_sites = guest_sites
                is_guest = false
                enableButton('register', 'light', true, 'إنشاء حساب جديد')
                signInFrontendUpdate()
                setAuthCookies(email, password)
            } else {
                // If registration fails, show alert and return.
                console.log('email is already in use.')
                showAlert('val', 'warning', 'البريد الالكتروني مستخدَم')
                enableButton('register', 'light', true, 'إنشاء حساب جديد')
            }
        }
    }

    params = `name=${name.replace(' ', '+')}&email=${email}&password=${password}&sites=${guest_sites.toString()}`
    httpRequest.open('POST', `${server_ip}/registration?${params}`, true);
    httpRequest.send();

}

/**
 * Validate sign in details.
 */
function signInValidation() {

    email = document.getElementById('inputEmail').value.trim()
    password = document.getElementById('inputPassword').value

    // If either email or password is empty, show alert.
    if (!validateEmail(email) || password === "") {
        console.log('invalid email.')
        showAlert('val', 'danger', 'البريد الالكتروني أو كلمة السر غير صحيحة')
        return false
    }

    console.log(email + ':' + password)
    signIn(email, password)
}

/**
 * Attempt signing in.
 * @param  {string} email The user's email.
 * @param  {string} password The user's password.
 */
function signIn(email, password) {

    enableButton('login', 'light', false, 'تسجيل الدخول')

    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === 4) {
            console.log(httpRequest.response)
            console.log(typeof (httpRequest.response))
            // If either information is incorrect, show alert.
            if (httpRequest.response == "Unauthorized Access") {
                enableButton('login', 'light', true, 'تسجيل الدخول')
                showAlert('val', 'danger', 'البريد الالكتروني أو كلمة السر غير صحيحة')
            } else {
                // Otherwise, sign in and update global information.
                response = JSON.parse(httpRequest.response)
                global_name = response['name']
                global_email = email
                global_password = password
                global_sites = response['sites']
                is_guest = false
                enableButton('login', 'light', true, 'تسجيل الدخول')
                setAuthCookies(email, password)
                signInFrontendUpdate()
            }
        }
    }

    httpRequest.open('GET', `${server_ip}/validation`, true);
    httpRequest.withCredentials = true;
    httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${email}:${password}`));
    httpRequest.send();
}

function setAuthCookies(email, password) {
    document.cookie = "email" + "=" + encodeURIComponent(email)
    document.cookie = "password" + "=" + encodeURIComponent(password)
}

/**
 * Update frontend after sign in.
 */
function signInFrontendUpdate() {
    $('#validationModal').modal('hide')
    console.log(`Welcome ${global_name}`)

    // Hide sign in button.
    signInButton = document.getElementById("signInButton")
    signInButton.style.display = "none"

    // Hide homepage sign in button.
    signInButtonHome = document.getElementById("signInButtonHome")
    signInButtonHome.style.display = "none"

    // Unhide name dropdown button.
    nameDropdown = document.getElementById("nameDropdown")
    nameDropdown.style.display = ""

    // Unhide homepage name dropdown button.
    nameDropdownHome = document.getElementById("nameDropdownHome")
    nameDropdownHome.style.display = ""

    // Rename dropdown button to user's name.
    nameDropdownMenu = document.getElementById("nameDropdownMenu")
    nameDropdownMenu.innerHTML = `${global_name.charAt(0)}`

    // Rename homepage dropdown button to user's name.
    nameDropdownMenuHome = document.getElementById("nameDropdownMenuHome")
    nameDropdownMenuHome.innerHTML = `${global_name}`

    // Show stars next to answers, if they exist.
    if (document.getElementById('results').innerHTML != "") {
        updateStarButtonDisplay()
    }

    // Update settings update name and email text field placeholders.
    document.getElementById('updateNameInput').placeholder = global_name
    document.getElementById('updateEmailInput').placeholder = global_email
}

/**
 * Sign out.
 */
function signOut() {

    // Empty global details.
    global_sites = guest_sites
    global_name = ""
    global_email = ""
    global_password = ""

    // Unhide sign in button.
    signInButton = document.getElementById("signInButton")
    signInButton.style.display = ""

    // Hide name dropdown button.
    nameDropdown = document.getElementById("nameDropdown")
    nameDropdown.style.display = "none"

    // Clear name dropdown button text.
    nameDropdownMenu = document.getElementById("nameDropdownMenu")
    nameDropdownMenu.innerHTML = `${global_name}`

    setAuthCookies("","")

    // Reload webpage.
    location.reload()
}

function toggleBetweenSites(clickedBy) {

    sitesModalButton = document.getElementById("sitesModalButton")

    if (clickedBy == 'specific') {
        sitesModalButton.disabled = false

        document.getElementById("sitesModalButton").classList.remove('btn-outline-secondary');
        document.getElementById("sitesModalButton").classList.add('btn-outline-info');
    }
    else if (clickedBy == 'all') {
        sitesModalButton.disabled = true

        document.getElementById("sitesModalButton").classList.add('btn-outline-secondary');
        document.getElementById("sitesModalButton").classList.remove('btn-outline-info');
    }
}


function deleteSite(site_name) {
    for (var i = 0; i < draft_sites.length; i++) {
        if (draft_sites[i] === site_name) {
            console.log('found ' + draft_sites[i])
            draft_sites.splice(i, 1);
        }
    }
    // if (!is_guest) {
    //     updateSitesList()
    // }
    showSitesList()
}

function addSite(site_name) {

    if (site_name.trim().length == 0) {
        return
    }

    try {
        site = new URL(site_name)
    } catch (err) {
        console.log(err.message)
        showAlert('sites', 'warning', 'صيغة الموقع غير صحيحة')
        return
    }

    site = site.origin
    console.log(site)

    if (draft_sites.includes(site)) {
        showAlert('sites', 'warning', 'الموقع مُدْرَج في القائمة')
        console.log('Site already included.')
        return
    }

    // if (!validateWebsite(site_name)) {
    //     showAlert('sites', 'warning', 'Website format is invalid')
    //     console.log('Invalid Website')
    //     return
    // }

    draft_sites.push(site)
    showSitesList()
    // if (!is_guest) {
    //     updateSitesList()
    // }
}

function resetSitesList() {
    draft_sites = [...default_sites]
    showSitesList()
}

function updateSitesList() {

    global_sites = [...draft_sites]

    if (is_guest) {
        $('#sitesModal').modal('hide')
        return
    }

    enableButton('sites', 'success', false, 'حفظ التغييرات')

    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === 4) {
            console.log(httpRequest.response)
            enableButton('sites', 'success', true, 'حفظ التغييرات')
            $('#sitesModal').modal('hide')

            // console.log(typeof(httpRequest.response))
            // return JSON.parse(httpRequest.response)
        }
    }

    httpRequest.open('PUT', `${server_ip}/sites?sites=${global_sites.toString()}`, true);
    httpRequest.withCredentials = true;
    httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${global_email}:${global_password}`));
    httpRequest.send();
}

function getSitesList() {

    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === 4) {
            console.log(httpRequest.response)
            console.log(typeof (httpRequest.response))
            return JSON.parse(httpRequest.response)
        }
    }

    httpRequest.open('GET', `${server_ip}/sites`, true);
    httpRequest.withCredentials = true;
    httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${global_email}:${global_password}`));
    httpRequest.send();
}

function loadSitesList() {

    draft_sites = [...global_sites]
    showSitesList()

}

function showSitesList() {

    sites_table_body = document.getElementById('sitesTableBody')
    sites_table_body.innerHTML = ""
    draft_sites.forEach(element => {
        console.log(element)
        var table_row = document.createElement("tr")

        var td1 = document.createElement("td")
        site_name = document.createTextNode(element)
        td1.appendChild(site_name)
        table_row.appendChild(td1)

        var td2 = document.createElement("td")
        td2.className = "text-right align-middle"
        var delete_button = document.createElement("button")
        delete_button.type = "button"
        delete_button.onclick = function () {
            deleteSite(element)
        }
        delete_button.className = "btn btn-outline-danger"

        // var trash = document.createElement("img")
        // trash.className = "text-left"
        // trash.src = "./images/trash.png"
        // trash.width = "20"
        // trash.height = "20"
        // delete_button.appendChild(trash)

        delete_button.innerHTML = `
        <i class="bi bi-trash"></i>
        `
        td2.appendChild(delete_button)
        table_row.appendChild(td2)

        sites_table_body.appendChild(table_row)
    });

    var table_row = document.createElement("tr")
    var td1 = document.createElement("td")
    var site_input = document.createElement("input")
    site_input.className = "form-control"
    site_input.type = "text"
    site_input.id = "newSite"
    site_input.dir = "ltr"
    td1.appendChild(site_input)
    table_row.appendChild(td1)

    var td2 = document.createElement("td")
    td2.className = "text-right align-middle"
    var add_button = document.createElement("button")
    add_button.className = "btn btn-outline-success text-right align-middle"
    add_button.type = "button"
    add_button.innerHTML = `
        <i class="bi bi-plus-lg"></i>
    `
    add_button.onclick = function () {
        addSite(document.getElementById('newSite').value)
    }
    td2.appendChild(add_button)
    table_row.appendChild(td2)

    sites_table_body.appendChild(table_row)
}

function submitQuery() {

    start_time = Date.now()

    var query = document.getElementById('inputSearchOne').value

    if (query.trim().length == 0) {
        query = document.getElementById('inputSearchTwo').value
        if (query.trim().length == 0) {
            return
        }
    }

    current_query = query

    var language = 'ar';
    var sites = global_sites;

    makeRequest(query, language, sites, 1)

    console.log(query)
    console.log(language)
    console.log(sites)
}

function submitQueryHome() {

    start_time = Date.now()

    var query = document.getElementById('inputSearchHome').value

    if (query.trim().length == 0) {
        return
    }

    current_query = query

    var language = 'ar';
    var sites = global_sites;

    makeRequest(query, language, sites, 1)

    console.log(query)
    console.log(language)
    console.log(sites)
}

var start_index = 11

function loadMoreAnswers() {

    var language = 'ar';
    var sites = global_sites;

    makeRequest(current_query, language, sites, start_index)

    console.log(current_query)
    console.log(language)
    console.log(sites)

    start_index += 10
}

function changeToRegular() {

    console.log('changing to regular')

    homepage = document.getElementById("homepage")
    homepage.style.display = 'none'

    navBarSearch = document.getElementById("navBarSearchOne")
    navBarSearch.style.display = ''

    navBarSearch = document.getElementById("navBarSearchTwo")
    navBarSearch.style.display = ''

    inputSearchHomeValue = document.getElementById('inputSearchHome').value
    document.getElementById('inputSearchOne').value = inputSearchHomeValue
    document.getElementById('inputSearchTwo').value = inputSearchHomeValue

    footerHome = document.getElementById('footerHome')
    footerHome.style.display = 'none'

    loadMore = document.getElementById('loadMore')
    loadMore.style.display = ''

    navBarHomepage = document.getElementById("navBarHomepage")
    navBarHomepage.style.display = 'none'
}

function changeToHome() {

    console.log('changing to home')

    homepage = document.getElementById("homepage")
    homepage.style.display = ''

    navBarSearch = document.getElementById("navBarSearchOne")
    navBarSearch.style.display = 'none'

    navBarSearch = document.getElementById("navBarSearchTwo")
    navBarSearch.style.display = 'none'

    document.getElementById('inputSearchOne').value = ""
    document.getElementById('inputSearchTwo').value = ""
    document.getElementById('inputSearchHome').value = ""
    
    current_query = ""

    footerHome = document.getElementById('footerHome')
    footerHome.style.display = ''

    loadMore = document.getElementById('loadMore')
    loadMore.style.display = 'none'

    navBarHomepage = document.getElementById("navBarHomepage")
    navBarHomepage.style.display = ''

    document.getElementById('results').innerHTML = ""
}

function enableButton(type, spinner_type, enabled, text) {
    typeButton = document.getElementById(`${type}Button`)
    typeButton.disabled = !enabled;
    if (enabled) {
        typeButton.innerHTML = text
    } else {
        typeButton.innerHTML = `<div class='spinner-border spinner-border-sm my-1 text-${spinner_type}' role='status'><span class='sr-only'>Loading...</span></div>`
    }
}

function makeRequest(query, language, sites, start) {

    enableButton('searchOne', 'light', false, `<i class="bi bi-search"></i>`)
    enableButton('searchTwo', 'light', false, `<i class="bi bi-search"></i>`)
    enableButton('searchHome', 'light', false, `<i class="bi bi-search"></i>`)
    enableButton('loadMore', 'light', false, `اعرض المزيد`)

    var query = query.replace(' ', '+')

    if (is_specific) {
        var params = `query=${query}&language=${language}&sites=${sites.toString()}&start=${start}`
    } else {
        var params = `query=${query}&language=${language}&sites=&start=${start}`
    }

    if (answer_extraction) {
        params = params + `&extract=1`
    } else {
        params = params + `&extract=0`
    }

    if (bert_reranking) {
        params = params + `&rerank=1`
    } else {
        params = params + `&rerank=0`
    }

    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status == 200) {
                enableButton('searchOne', 'light', true, `<i class="bi bi-search"></i>`)
                enableButton('searchTwo', 'light', true, `<i class="bi bi-search"></i>`)
                enableButton('searchHome', 'light', true, `<i class="bi bi-search"></i>`)
                enableButton('loadMore', 'light', true, `اعرض المزيد`)

                if (JSON.parse(httpRequest.response).results.length == 0) {
                    showAlert('main', 'danger', 'No results found. Make sure your query is in Arabic.')
                    return
                }

                processResponse(httpRequest.response, start == 1)

                if (document.getElementById("homepage").style.display != 'none')
                    changeToRegular()
                end_time = Date.now()
                console.log("time= " + (end_time-start_time))
                return
            }
            enableButton('searchOne', 'light', true, `<i class="bi bi-search"></i>`)
            enableButton('searchTwo', 'light', true, `<i class="bi bi-search"></i>`)
            enableButton('searchHome', 'light', true, `<i class="bi bi-search"></i>`)
            enableButton('loadMore', 'light', true, `اعرض المزيد`)
            showAlert('main', 'danger', 'هناك خلل، حاول مرة أخرى')
            console.log(httpRequest.status)
            console.log(httpRequest.response)

        }
    }

    httpRequest.open('GET', `${server_ip}/search?${params}`, true);
    console.log(`${server_ip}/search?${params}`)
    httpRequest.withCredentials = true;
    httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${global_email}:${global_password}`));
    httpRequest.send();
}

function updateLog(query, url, action) {

    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status == 200) {
                console.log("logging successful.")
            } else {
                console.log("logging failed.")
            }
            return true
        }
    }

    httpRequest.open('POST', `${server_ip}/log?query=${encodeURIComponent(query)}&url=${encodeURIComponent(url)}&action=${encodeURIComponent(action)}`, true);
    httpRequest.withCredentials = true;
    httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${global_email}:${global_password}`));
    httpRequest.send();
}

function processResponse(response, clear) {
    var response = JSON.parse(response)
    var results = response.results;

    document.getElementById("mainAlertSpace").innerHTML = ""

    var element = document.getElementById("results");
    if (clear) {
        element.innerHTML = ""
    }

    for (i in results) {

        console.log(results[i].link)
        // console.log(typeof (results[i].link))
        domain = (new URL(results[i].link))
        domain = domain.hostname.replace('www.', '')

        google_rank = results[i].google_rank
        if (bert_reranking) {
            bert_rank = results[i].bert_rank
        } else {
            bert_rank = 0
        }

        answer = results[i].snippet
        is_already_saved = results[i].is_already_saved
        // console.log(is_already_saved)

        if (answer_extraction) {
            if (results[i].matches.length > 0) {
                answer = integrateVerses(results[i].snippet, results[i].matches, results[i].link)
            }
        }

        j = 0
        do {
            if (answer.length - snippet_length > 50) {
                local_snippet_length = snippet_length + (30 * j)
            } else {
                local_snippet_length = answer.length
            }
            snippet = answer.substring(0, local_snippet_length)
            var span_start_count = (snippet.match(/<span/g) || []).length;
            console.log(span_start_count)
            var span_end_count = (snippet.match(/<\/span>/g) || []).length;
            console.log(span_end_count)
            j += 1
        } while (span_start_count != span_end_count)

        // if (span_start_count > span_end_count) {
        //     console.log(snippet)
        //     snippet = snippet + "</span>"
        // }
        // window.open('${results[i].link}', '_blank').focus(); 

        var card = document.createElement("div")
        card.className = "card my-3 text-dark"
        card.style = "background-color: #ffffffc4;"
        card.innerHTML = `
        <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h5 class="card-title"><a class="green-title green-link" data-toggle="tooltip" data-placement="bottom" data-html="true" title="${rankingToolipText(i, google_rank, bert_rank)}"><i class="bi bi-info-circle"></a></i>&ensp;<a href="${results[i].link}" target=”_blank” id="resultTitle${i}" class="green-link green-title" onclick="updateLog('${current_query}','${results[i].link}','CLK'); return true">${results[i].title}</a></h5>
                    <h6 class="card-subtitle text-muted">${domain}</h6>
                </div>
                <button type="button" class="btn ${is_already_saved ? "btn-info" : "btn-outline-info"} button-star" onclick="saveAnswer(${i})" id="saveButton${i}" style="display: ${starButtonDisplay()}"><i class="bi ${is_already_saved ? "bi-star-fill" : "bi-star"}"></i></button>
            </div>
        </div>
        <div class="card-body">
            <div class="card-text" id="snippetedText${i}">
                ${snippet}${answer.length > snippet.length ? `... <a href='javascript:toggleSnippet(${i});' class='green-title green-link'>[المزيد]</a>` : ""}
            </div>
            <div class="card-text" id="fullText${i}" style="display: none">
            <span id="resultText${i}">${answer}</span> <a href="javascript:toggleSnippet(${i});" class="green-title green-link">[طي]</a>
            </div>
        </div>
        `
        element.appendChild(card)
    }

    verses = document.getElementsByClassName("verse-shell")
    if(verses_extraction) {
        for (let i = 0; i < verses.length; i++) {
            verses[i].classList.add('verse')
        }
    } else {
        for (let i = 0; i < verses.length; i++) {
            verses[i].classList.remove('verse')
        }
    }
    
    hadiths = document.getElementsByClassName("hadith-shell")
    if(hadith_extraction) {
        for (let i = 0; i < hadiths.length; i++) {
            hadiths[i].classList.add('hadith')
        }
    } else {
        for (let i = 0; i < hadiths.length; i++) {
            hadiths[i].classList.remove('hadith')
        }
    }
}

function integrateVerses(result, matches, url) {

    if (matches.length > 0) {

        console.log(matches)

        resultArraySplit = result.split(String.fromCharCode(160)).join(" ").split(" ")

        resultArray = []

        resultArraySplit.forEach(element => {
            if (element !== '') {
                resultArray.push(element);
            }
          });

        // for (let i = 0; i < resultArray.length; i++) {
        //     resultArray[i] = i + resultArray[i];
        // }

        for (let i = matches.length - 1; i >= 0; i--) {
    
            endIndex = matches[i].endInText
            resultArray.splice(endIndex, 0, '</span>')
    
            startIndex = matches[i].startInText
            // resultArray.splice(startIndex, 0, `<span class='verse' data-toggle='tooltip' data-placement='left' data-html='true' title='${matches[i].aya_name}'>`)
            
            console.log(matches[i].tag)
            
            if (matches[i].tag == "quran") {
                tooltipText = `
                <small>
                <b>${matches[i].aya_name}</b> : ${matches[i].aya_start}${matches[i].aya_end > matches[i].aya_start ? "-"+matches[i].aya_end : ""}
                </small>
                `
                resultArray.splice(startIndex, 0, `<span class='verse verse-shell' onmouseenter="updateLog('${current_query}', '${url}', 'HVR')"><span class='tooltip-span'>${tooltipText}</span>`)
            } else {
                console.log(matches[i])
                reference = matches[i].ref
                // "كتاب":ref.bk_name
                // "باب":ref.ch_name
                // "قسم":ref.sec_name
                // "رقم الحديث":ref.num
                // "الدرجة":ref.grade
                tooltipText = `
                <small>
                <b>${reference.bk_name}</b>
                `
                if (reference.ch_name != "nan") {
                    tooltipText = tooltipText + `
                    <br>
                    ${reference.ch_name}
                    `
                }
                if (reference.sec_name != "nan") {
                    tooltipText = tooltipText + `
                    <br>
                    ${reference.sec_name}
                    `
                }
                if (reference.num != "nan") {
                    tooltipText = tooltipText + `
                    <br>
                    رقم الحديث: ${reference.num}
                    `
                }
                if (reference.grade != "nan") {
                    tooltipText = tooltipText + `
                    <br>
                    الدرجة: ${reference.grade}
                    `
                }
                tooltipText = tooltipText + `
                </small>
                `
                resultArray.splice(startIndex, 0, `<span class='hadith hadith-shell' onmouseenter="updateLog('${current_query}', '${url}', 'HVR')"><span class='tooltip-span'>${tooltipText}</span>`)
            }
        }

        result = resultArray.join(" ")
    }

    return result
}

function rankingToolipText(i, google_rank, bert_rank) {
    // Calculate rank.
    rank = parseInt(i) + 1 

    // <i class='bi bi-google'></i> 

    return `
    تصنيف <b>Google</b>: ${google_rank}
        ${(bert_rank == 0) ? '<br>تصنيف <b>BERT</b> غير مفعل': '<br>تصنيف <b>BERT</b>: ' + bert_rank}
    `
}

function starButtonDisplay() {
    if (is_guest) {
        return 'none'
    } else {
        return ''
    }
}

function updateStarButtonDisplay() {
    starButtons = document.getElementsByClassName("button-star")
    for (let index = 0; index < starButtons.length; index++) {
        if (is_guest) {
            starButtons[index].style.display = "none"
        } else {
            starButtons[index].style.display = ""
        }
    }
}

function toggleSnippet(i) {
    snippetedText = document.getElementById(`snippetedText${i}`)
    fullText = document.getElementById(`fullText${i}`)

    resultTitle = document.getElementById(`resultTitle${i}`)

    if (snippetedText.style.display == 'none') {
        snippetedText.style.display = ''
        fullText.style.display = 'none'
        updateLog(current_query, resultTitle.href, 'COL')
    } else {
        snippetedText.style.display = 'none'
        fullText.style.display = ''
        updateLog(current_query, resultTitle.href, 'EXP')
    }
}

function saveAnswer(i) {

    resultText = document.getElementById(`resultText${i}`).innerHTML
    resultURL = document.getElementById(`resultTitle${i}`).href
    saveButton = document.getElementById(`saveButton${i}`)

    query = current_query

    if (saveButton.className == `btn btn-outline-info button-star`) {
        console.log(resultText)
        saveButton.className = `btn btn-info button-star`
        saveButton.innerHTML = `<i class="bi bi-star-fill"></i>`
        saveAnswerToBackend(query, resultText, resultURL)
    } else {
        saveButton.className = `btn btn-outline-info button-star`
        saveButton.innerHTML = `<i class="bi bi-star"></i>`
        deleteSingleAnswerToBackend(resultURL)
    }
}

function saveAnswerToBackend(query, answer, url) {

    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === 4) {
            console.log(httpRequest.response)
            response = JSON.parse(httpRequest.response)
            console.log(response)
        }
    }

    httpRequest.open('POST', `${server_ip}/saved?&query=${encodeURIComponent(query)}&url=${encodeURIComponent(url)}`, true);
    httpRequest.withCredentials = true;
    httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${global_email}:${global_password}`));
    httpRequest.send();
}

function updateName() {
    updateNameInput = document.getElementById("updateNameInput")
    updatedName = updateNameInput.value.trim()
    if (updatedName.length === 0) {
        return
    } else {
        enableButton('updateName', 'success', false, 'تحديث')

        var httpRequest = new XMLHttpRequest();
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === 4) {
                response = JSON.parse(httpRequest.response)
                if (response['updated']) {
                    global_name = updatedName
                    nameDropdownMenu = document.getElementById("nameDropdownMenu")
                    nameDropdownMenu.innerHTML = `${global_name}`
                    document.getElementById('updateNameInput').placeholder = global_name
                    document.getElementById('updateNameInput').value = ''
                    document.getElementById('nameDropdownMenuHome').innerHTML = `${global_name}`
                    showAlert('profile', 'success', 'تم تحديث الاسم')
                }
                enableButton('updateName', 'success', true, 'تحديث')
            }
        }

        httpRequest.open('PUT', `${server_ip}/update?label=name&value=${encodeURIComponent(updatedName)}`, true);
        httpRequest.withCredentials = true;
        httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${global_email}:${global_password}`));
        httpRequest.send();
    }
}

function updateEmail() {
    updateEmailInput = document.getElementById("updateEmailInput")
    updatedEmail = updateEmailInput.value.trim()
    if (updatedEmail.length === 0) {
        return
    } else if (!validateEmail(updatedEmail)) {
        showAlert('profile', 'warning', 'صيغة البريد الالكتروني غير صحيحة')

    } else {
        enableButton('updateEmail', 'success', false, 'تحديث')

        var httpRequest = new XMLHttpRequest();
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === 4) {
                response = JSON.parse(httpRequest.response)
                if (response['updated']) {
                    global_email = updatedEmail
                    document.getElementById('updateEmailInput').placeholder = updatedEmail
                    document.getElementById('updateEmailInput').value = ''
                    showAlert('profile', 'success', 'تم تحديث البريد الالكتروني')
                    setAuthCookies(global_email, global_password)
                } else {
                    showAlert('profile', 'danger', 'البريد الالكتروني مستخدَم')
                }
                enableButton('updateEmail', 'success', true, 'تحديث')
            }
        }

        httpRequest.open('PUT', `${server_ip}/update?label=email&value=${encodeURIComponent(updatedEmail)}`, true);
        httpRequest.withCredentials = true;
        httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${global_email}:${global_password}`));
        httpRequest.send();
    }
}

function updatePassword() {
    updateOldPasswordInput = document.getElementById("updateOldPasswordInput")
    if (updateOldPasswordInput.value != global_password) {
        showAlert('security', 'danger', 'كلمة السر غير صحيحة')
        return
    }

    updatePasswordInput = document.getElementById("updatePasswordInput")
    updateConfirmPasswordInput = document.getElementById("updateConfirmPasswordInput")

    if (updatePasswordInput.value != updateConfirmPasswordInput.value) {
        showAlert('security', 'warning', 'كلمة السر غير مطابقة')
        return
    }

    if (updatePasswordInput.value.length < 8) {
        showAlert('security', 'warning', 'كلمة السر يجب أن تكون من 8 خانات على الأقل')
        return
    }

    updatedPassword = updatePasswordInput.value
    enableButton('updatePassword', 'success', false, 'تحديث')

    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {

        if (httpRequest.readyState === 4) {
            response = JSON.parse(httpRequest.response)
            if (response['updated']) {
                global_password = updatedPassword
                updateOldPasswordInput.value = ''
                updatePasswordInput.value = ''
                updateConfirmPasswordInput.value = ''
                showAlert('security', 'success', 'تم تحديث كلمة السر')
                setAuthCookies(global_email, global_password)
            }
            enableButton('updatePassword', 'success', true, 'تحديث')
        }
    }

    httpRequest.open('PUT', `${server_ip}/update?label=password&value=${encodeURIComponent(updatedPassword)}`, true);
    httpRequest.withCredentials = true;
    httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${global_email}:${global_password}`));
    httpRequest.send();
}

function deleteAccountWarning() {
    $('#settingsModal').modal('hide')
}

function deleteAccount() {
    inputDeletePassword = document.getElementById("inputDeletePassword").value

    if (inputDeletePassword == global_password) {
        enableButton('deleteAccount', 'light', false, 'حذف الحساب')

        var httpRequest = new XMLHttpRequest();
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === 4) {
                response = JSON.parse(httpRequest.response)
                if (response['deleted']) {
                    enableButton('deleteAccount', 'light', true, 'حذف الحساب')
                    signOut()
                } else {
                    enableButton('deleteAccount', 'light', true, 'حذف الحساب')
                    showAlert('deleteAccount', 'danger', 'محاولة حذف الحساب فاشلة')
                }
            }
        }

        httpRequest.open('DELETE', `${server_ip}/account`, true);
        httpRequest.withCredentials = true;
        httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${global_email}:${inputDeletePassword}`));
        httpRequest.send();
    } else {
        showAlert('deleteAccount', 'danger', 'كلمة السر غير صحيحة')
    }
}


function showAlert(section, type, message) {
    alertSpace = document.getElementById(`${section}AlertSpace`)
    alertSpace.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
        ${message}
    </div>
    `
}

function validateWebsite(site_name) {
    var pattern = new RegExp('^(https?:\\/\\/)?' + // protocol
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
        '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
        '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
        '(\\#[-a-z\\d_]*)?$', 'i'); // fragment locator
    return !!pattern.test(site_name);
}

function validateEmail(email_address) {
    return (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email_address))
}

function loadHistory() {

    var historyTableBody = document.getElementById('historyTableBody')
    historyTableBody.innerHTML = `
        <div class='spinner-border spinner-border-sm my-1 text-primary' role='status'><span class='sr-only'>Loading...</span></div>
    `

    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === 4) {
            console.log(httpRequest.response)
            response = JSON.parse(httpRequest.response)
            searchHistory = response['history']

            console.log('searchHistory')
            console.log(searchHistory)

            updateHistoryTable(searchHistory)
        }
    }

    httpRequest.open('GET', `${server_ip}/history`, true);
    httpRequest.withCredentials = true;
    httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${global_email}:${global_password}`));
    httpRequest.send();
}

function updateHistoryTable(searchHistory) {

    searchHistory.reverse()

    var historyTableBody = document.getElementById('historyTableBody')

    if (searchHistory.length == 0) {
        historyTableBody.innerHTML = `<span class='text-muted'>لا توجد سجلات بحث محفوظة</span>`
    } else {
        historyTableBody.innerHTML = ''
    }

    for (let index = 0; index < searchHistory.length; index++) {

        // console.log(typeof (searchHistory[index]['time']))
        historyTime = new Date(searchHistory[index]['time'].replace(' ', 'T'))
        console.log(typeof (historyTime))
        console.log(historyTime)
        // historyTime = historyTime.getTime() - offset*60000
        console.log(historyTime)

        var row = document.createElement('tr')
        row.id = `history${index}`
        row.className = 'align-bottom'
        row.innerHTML = `
            <td class="text-left align-middle"><a href="javascript:searchFromHistory(${index});">${searchHistory[index]['query']}</a></td>
            <td class="text-left align-middle text-muted text-monospace" dir="ltr">${formatDateTime(historyTime)}</td>
            <td class="text-right"><button type="button" class='btn btn-outline-danger text-center' onclick='deleteHistory(${index})'><i class="bi bi-trash"></i></button></td>
        `

        historyTableBody.appendChild(row)
    }
}

function formatDateTime(date) {
    // return `${date.getFullYear()}/${getMonth(date)}/${date.getDate()}\t\t${getHour(date)}:${getMinutes(date)}`
    return `${date.getDate()} ${getMonth(date)} ${date.getFullYear()}\t\t${getHour(date)}:${getMinutes(date)}`
}

function getHour(date) {

    hour = date.getHours()

    if (hour < 10) {
        return `0${hour}`
    }
    
    return hour
}

function getMonth(date) {

    month = "NaN"

    switch (date.getMonth() + 1) {
        case 1:
            month = "January";
            break;
        case 2:
            month = "February";
            break;
        case 3:
            month = "March";
            break;
        case 4:
            month = "April";
            break;
        case 5:
            month = "May";
            break;
        case 6:
            month = "June";
            break;
        case 7:
            month = "July";
            break;
        case 8:
            month = "August";
            break;
        case 9:
            month = "September";
            break;
        case 10:
            month = "October";
            break;
        case 11:
            month = "November";
            break;
        case 12:
            month = "December";
      }

    return month
}

function getMinutes(date) {

    min = date.getMinutes()

    if (min < 10) {
        return `0${min}`
    }
    
    return min
}

function searchFromHistory(index) {
    query = searchHistory[index]['query']
    $('#searchHistoryModal').modal('hide')

    if (query.trim().length == 0) {
        return
    }

    var sites = global_sites;

    if (document.getElementById('navBarSearch').style.display == 'none') {
        document.getElementById('inputSearchHome').value = query
    } else {
        document.getElementById('inputSearchOne').value = query
        document.getElementById('inputSearchTwo').value = query
    }

    makeRequest(query, 'ar', sites, 1)

    console.log(query)
    console.log(sites)
}

function deleteHistory(index) {

    query = searchHistory[index]['query']
    time = searchHistory[index]['time']

    if (index < searchHistory.length) {
        searchHistory.splice(index, 1);
    }

    updateHistoryTable(searchHistory)

    deleteSingleHistoryToBackend(query, time)
}

function deleteSingleHistoryToBackend(query, time) {

    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === 4) {
            console.log(httpRequest.response)
            response = JSON.parse(httpRequest.response)
            deleted = response['deleted']
            console.log(deleted)
        }
    }

    httpRequest.open('DELETE', `${server_ip}/history?query=${encodeURIComponent(query)}&date=${encodeURIComponent(time)}`, true);
    httpRequest.withCredentials = true;
    httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${global_email}:${global_password}`));
    httpRequest.send();
}

function clearAllHistory() {

    searchHistory = []

    updateHistoryTable(searchHistory)

    clearAllHistoryToBackend()
}

function clearAllHistoryToBackend() {

    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === 4) {
            console.log(httpRequest.response)
            response = JSON.parse(httpRequest.response)
            deleted = response['deleted']
            console.log(deleted)
        }
    }

    httpRequest.open('DELETE', `${server_ip}/history`, true);
    httpRequest.withCredentials = true;
    httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${global_email}:${global_password}`));
    httpRequest.send();
}

function loadSavedAnswers() {
    var savedAnswersTableBody = document.getElementById('savedAnswersTableBody')
    savedAnswersTableBody.innerHTML = `
        <div class='spinner-border spinner-border-sm my-1 text-primary' role='status'><span class='sr-only'>Loading...</span></div>
    `
    
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === 4) {
            console.log(httpRequest.response)
            response = JSON.parse(httpRequest.response)
            savedAnswers = response['saved']

            updateSavedTable()
        }
    }

    httpRequest.open('GET', `${server_ip}/saved`, true);
    httpRequest.withCredentials = true;
    httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${global_email}:${global_password}`));
    httpRequest.send();
}

function updateSavedTable() {

    var savedAnswersTableBody = document.getElementById('savedAnswersTableBody')

    if (savedAnswers.length == 0) {
        savedAnswersTableBody.innerHTML = `<span class='text-muted'>لا توجد فتاوي محفوظة</span>`
    } else {
        savedAnswersTableBody.innerHTML = ''
    }

    for (let index = 0; index < savedAnswers.length; index++) {
        row = document.createElement('tr')
        row.id = `saved${index}`
        row.className = 'align-bottom'
        row.innerHTML = `
            <td class="text-left align-middle small text-muted">${savedAnswers[index]['query']}</td>
            <td rowspan=3 class="text-right align-middle border-bottom"><button type="button" class='btn btn-outline-danger text-center' onclick='deleteSavedAnswer(${index})'><i class="bi bi-trash"></i></button></td>
        `
        savedAnswersTableBody.appendChild(row)

        answer = savedAnswers[index]['response']
        matches = savedAnswers[index]['matches']

        console.log(answer)

        if (answer_extraction) {
            if (matches.length > 0) {
                answer = integrateVerses(answer, matches)
            }
        }

        j = 0
        do {
            if (answer.length - snippet_length > 50) {
                local_snippet_length = snippet_length + (30 * j)
            } else {
                local_snippet_length = answer.length
            }
            snippet = answer.substring(0, local_snippet_length)
            var span_start_count = (snippet.match(/<span/g) || []).length;
            console.log(span_start_count)
            var span_end_count = (snippet.match(/<\/span/g) || []).length;
            console.log(span_end_count)
            j += 1
        } while (span_start_count != span_end_count)

        row = document.createElement('tr')
        // row.id = `saved${index}`
        row.className = 'align-bottom'
        row.innerHTML = `
            <td class="text-left align-middle" id="savedAnswerSnippet${index}">
                ${snippet}${answer.length > snippet.length ? `... <a href="javascript:toggleSavedSnippet(${index})" class='green-title green-link'>[المزيد]</a>` : ""}
            </td>
            <td class="text-left align-middle" style="display: none" id="savedAnswerFull${index}">
                ${answer} <a href="javascript:toggleSavedSnippet(${index})">[طي]</a>
            </td>
        `
        savedAnswersTableBody.appendChild(row)

        row = document.createElement('tr')
        // row.id = `saved${index}`
        row.className = 'align-bottom'
        console.log(savedAnswers[index]['url'])
        console.log(typeof (savedAnswers[index]['url']))

        domain = new URL(savedAnswers[index]['url'])
        domain = domain.hostname.replace('www.', '');
        row.innerHTML = `
            <td class="text-left align-middle small border-bottom"><a href="${savedAnswers[index]['url']}">${domain}</a></td>
        `
        savedAnswersTableBody.appendChild(row)
    }
}

function toggleSavedSnippet(index) {
    if (document.getElementById(`savedAnswerFull${index}`).style.display == "none") {
        document.getElementById(`savedAnswerFull${index}`).style.display = ""
        document.getElementById(`savedAnswerSnippet${index}`).style.display = "none"
    } else {
        document.getElementById(`savedAnswerFull${index}`).style.display = "none"
        document.getElementById(`savedAnswerSnippet${index}`).style.display = ""
    }
}

function snippedResponse(response) {

    if (response.length > snippet_length) {
        for (let index = snippet_length; index < response.length; index++) {
            if (response.charAt(index) == "." || response.charAt(index) == "؟") {
                response = response.substring(0, index + 1)
                break
            }
        }
    }
    return response
}

function deleteSavedAnswer(index) {

    url = savedAnswers[index]['url']
    console.log('1')
    console.log(savedAnswers)

    if (index < savedAnswers.length) {
        savedAnswers.splice(index, 1);
        console.log('2')
        console.log(savedAnswers)
    }

    updateSavedTable()

    const answerTitles = document.querySelectorAll("a.green-title")

    for (let i = 0; i < answerTitles.length; i++) {
        if(answerTitles[i].href == url){
            resultTitleID = answerTitles[i].id
            console.log(resultTitleID)
            resultIndex = resultTitleID.replace('resultTitle','');
            saveButton = document.getElementById(`saveButton${resultIndex}`)
            saveButton.className = `btn btn-outline-info button-star`
            saveButton.innerHTML = `<i class="bi bi-star"></i>`
        }  
    }

    deleteSingleAnswerToBackend(url)
}

function deleteSingleAnswerToBackend(url) {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === 4) {
            console.log(httpRequest.response)
            response = JSON.parse(httpRequest.response)
            deleted = response['deleted']
            console.log(deleted)
        }
    }

    httpRequest.open('DELETE', `${server_ip}/saved?url=${encodeURIComponent(url)}`, true);
    httpRequest.withCredentials = true;
    httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${global_email}:${global_password}`));
    httpRequest.send();
}

function clearAllSavedAnswers() {
    console.log('delete all')

    savedAnswers = []

    updateSavedTable()

    clearAllSavedAnswersToBackend()
}

function clearAllSavedAnswersToBackend() {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === 4) {
            console.log(httpRequest.response)
            response = JSON.parse(httpRequest.response)
            deleted = response['deleted']
            console.log(deleted)
        }
    }

    httpRequest.open('DELETE', `${server_ip}/saved`, true);
    httpRequest.withCredentials = true;
    httpRequest.setRequestHeader("Authorization", "Basic " + btoa(`${global_email}:${global_password}`));
    httpRequest.send();
}

function updateSearchSettings() {

    searchAgain = false

    specificOption = document.getElementById('specificOption')
    allOption = document.getElementById('allOption')

    searchAgain = (specificOption.classList.contains('active') != is_specific)
    is_specific = specificOption.classList.contains('active')

    // if (specificOption.classList.contains('active')) {
    //     is_specific = true
    // } else {
    //     is_specific = false
    // }

    if (is_specific) {
        toggleBetweenSites('specific')
        specificOption.classList.add('active')
        allOption.classList.remove('active')
    } else {
        toggleBetweenSites('all')
        specificOption.classList.remove('active')
        allOption.classList.add('active')
    }

    toggleAnswerExtractionCheckbox = document.getElementById("toggleAnswerExtractionCheckbox")
    if (!searchAgain) {
        searchAgain = (toggleAnswerExtractionCheckbox.checked != answer_extraction)
    }
    answer_extraction = toggleAnswerExtractionCheckbox.checked

    toggleVersesExtractionCheckbox = document.getElementById("toggleVersesExtractionCheckbox")
    toggleHadithExtractionCheckbox = document.getElementById("toggleHadithExtractionCheckbox")

    verses_extraction = toggleVersesExtractionCheckbox.checked
    hadith_extraction = toggleHadithExtractionCheckbox.checked

    local_verses_extraction_choice = verses_extraction
    local_hadith_extraction_choice = hadith_extraction

    verses = document.getElementsByClassName("verse-shell")
    console.log(verses)
    
    if(verses_extraction) {
        for (let i = 0; i < verses.length; i++) {
            verses[i].classList.add('verse')
        }
    } else {
        for (let i = 0; i < verses.length; i++) {
            verses[i].classList.remove('verse')
        }
    }

    hadiths = document.getElementsByClassName("hadith-shell")
    console.log(hadiths)
    
    if(hadith_extraction) {
        for (let i = 0; i < hadiths.length; i++) {
            hadiths[i].classList.add('hadith')
        }
    } else {
        for (let i = 0; i < hadiths.length; i++) {
            hadiths[i].classList.remove('hadith')
        }
    }

    // if (toggleAnswerExtractionCheckbox.checked == true) {
    //     console.log('answer extraction on')
    //     answer_extraction = true
    // } else {
    //     console.log('answer extraction off')
    //     answer_extraction = false
    // }

    // if (answer_extraction) {
    //     fullOption = document.getElementById("fullOption")
    //     mediumOption = document.getElementById("mediumOption")
    //     noneOption = document.getElementById("noneOption")

    //     // if (fullOption.classList.contains('active')) {
    //     //     snippet_length = snippetLengths.full
    //     // } else if (mediumOption.classList.contains('active')) {
    //     //     snippet_length = isMobile ? snippetLengths.mediumMobile : snippetLengths.medium
    //     // } else {
    //     //     snippet_length = snippetLengths.none
    //     // }
    // }

    toggleRerankingCheckbox = document.getElementById("toggleRerankingCheckbox")

    if (!searchAgain) {
        searchAgain = (toggleRerankingCheckbox.checked != bert_reranking)
    }
    bert_reranking = toggleRerankingCheckbox.checked

    // if (toggleRerankingCheckbox.checked == true) {
    //     console.log('reranking on')
    //     bert_reranking = true
    // } else {
    //     console.log('reranking off')
    //     bert_reranking = false
    // }

    console.log("verses_extraction:", verses_extraction)
    console.log("hadith_extraction:", hadith_extraction)

    if (searchAgain) {
        submitQuery()
    }
}

// function toggleAnswerExtraction() {
//     toggleAnswerExtractionCheckbox = document.getElementById("toggleAnswerExtractionCheckbox")
//     lengthOptions = document.getElementById('lengthOptions').children
//     lengthOptionsTitle = document.getElementById('lengthOptionsTitle')
//     if (toggleAnswerExtractionCheckbox.checked == false) {
//         Array.from(lengthOptions).forEach(option => {
//             option.disabled = true
//             option.classList.remove("btn-outline-info")
//             option.classList.add("btn-outline-secondary")
//         })
//         lengthOptionsTitle.classList.add("text-secondary")
//     } else {
//         Array.from(lengthOptions).forEach(option => {
//             option.disabled = false
//             option.classList.add("btn-outline-info")
//             option.classList.remove("btn-outline-secondary")
//         })
//         lengthOptionsTitle.classList.remove("text-secondary")
//     }
// }

function fixSearchSettingsOptions() {
    specificOption = document.getElementById('specificOption')
    allOption = document.getElementById('allOption')

    if (is_specific) {
        toggleBetweenSites('specific')
        specificOption.classList.add('active')
        allOption.classList.remove('active')
    } else {
        toggleBetweenSites('all')
        specificOption.classList.remove('active')
        allOption.classList.add('active')
    }

    // fullOption = document.getElementById("fullOption")
    // mediumOption = document.getElementById("mediumOption")
    // noneOption = document.getElementById("noneOption")

    // if(snippet_length == snippetLengths.full) {
    //     fullOption.classList.add('active')
    //     mediumOption.classList.remove('active')
    //     noneOption.classList.remove('active')
    // } else if(snippet_length == snippetLengths.none) {
    //     fullOption.classList.remove('active')
    //     mediumOption.classList.remove('active')
    //     noneOption.classList.add('active')
    // } else {
    //     fullOption.classList.remove('active')
    //     mediumOption.classList.add('active')
    //     noneOption.classList.remove('active')
    // }

    toggleAnswerExtractionCheckbox = document.getElementById("toggleAnswerExtractionCheckbox")
    toggleRerankingCheckbox = document.getElementById("toggleRerankingCheckbox")

    toggleAnswerExtractionCheckbox.checked = answer_extraction

    toggleVersesCheckboxes()

    // toggleAnswerExtraction()
    toggleRerankingCheckbox.checked = bert_reranking
}

function resetSearchSettingsToDefault() {

    specificOption = document.getElementById('specificOption')
    allOption = document.getElementById('allOption')

    is_specific = default_is_specific
    if (default_is_specific) {
        toggleBetweenSites('specific')
        specificOption.classList.add('active')
        allOption.classList.remove('active')
    } else {
        toggleBetweenSites('all')
        specificOption.classList.remove('active')
        allOption.classList.add('active')
    }

    // fullOption = document.getElementById("fullOption")
    // fullOption.classList.remove('active')
    // mediumOption = document.getElementById("mediumOption")
    // if (!mediumOption.classList.contains('active')) {
    //     mediumOption.classList.add('active')
    // }
    // noneOption = document.getElementById("noneOption")
    // noneOption.classList.remove('active')

    toggleAnswerExtractionCheckbox = document.getElementById("toggleAnswerExtractionCheckbox")
    toggleRerankingCheckbox = document.getElementById("toggleRerankingCheckbox")

    toggleAnswerExtractionCheckbox.checked = default_answer_extraction
    // toggleAnswerExtraction()

    local_verses_extraction_choice = default_verses_extraction
    local_hadith_extraction_choice = default_hadith_extraction
    toggleVersesCheckboxes()

    toggleRerankingCheckbox.checked = default_bert_reranking
}

function toggleVersesCheckboxes() {

    toggleAnswerExtractionCheckbox = document.getElementById("toggleAnswerExtractionCheckbox")
    
    toggleVersesExtractionCheckbox = document.getElementById("toggleVersesExtractionCheckbox")
    toggleHadithExtractionCheckbox = document.getElementById("toggleHadithExtractionCheckbox")

    toggleVersesExtractionText = document.getElementById("toggleVersesExtractionText")
    toggleHadithExtractionText = document.getElementById("toggleHadithExtractionText")

    if (!toggleAnswerExtractionCheckbox.checked) {

        local_verses_extraction_choice = toggleVersesExtractionCheckbox.checked
        local_hadith_extraction_choice = toggleHadithExtractionCheckbox.checked

        toggleVersesExtractionCheckbox.checked = false
        toggleHadithExtractionCheckbox.checked = false

        toggleVersesExtractionText.classList.add("text-secondary")
        toggleHadithExtractionText.classList.add("text-secondary")
    } else {

        toggleVersesExtractionCheckbox.checked = local_verses_extraction_choice
        toggleHadithExtractionCheckbox.checked = local_hadith_extraction_choice

        toggleVersesExtractionText.classList.remove("text-secondary")
        toggleHadithExtractionText.classList.remove("text-secondary")
    }
    
    toggleVersesExtractionCheckbox.disabled = !toggleAnswerExtractionCheckbox.checked
    toggleHadithExtractionCheckbox.disabled = !toggleAnswerExtractionCheckbox.checked
}