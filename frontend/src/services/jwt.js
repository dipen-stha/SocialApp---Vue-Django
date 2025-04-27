import Cookies from "js-cookie";

const accessToken = "access";
const refreshToken = "refresh";

const setToken = function (token) {
    Cookies.set("access", token)
};

const setRefreshToken = function (refresh) {
    Cookies.set("refresh", refresh)
};

const getToken = function () {
    const token = Cookies.get(accessToken);
    return token
};

const getRefreshToken = function () {
    const refresh = Cookies.get(refreshToken);
    return refresh
};

const destroyToken = function () {
    Cookies.remove(accessToken);
    Cookies.remove(refreshToken);
}

const jwtServices = {
    setToken,
    setRefreshToken,
    getToken,
    getRefreshToken,
    destroyToken
};

export default jwtServices;