import {createStore, mapState} from "vuex";

const store = createStore({
    state: {
        navWidth: 200, // 导航宽度
        windowInsets: { // 窗口数据
            height: 0,
            width: 0
        },
        navMenuIsClosed: false, // navMenu 是否折叠状态
        isInMobile: false, // 是否是手机端
        isShowingMenuToggleBtn: false, // 是否显示移动端的菜单切换按钮
        authorization: null, // authorization
        userData: null
    },
    getters: {
        isInPortraitMode: state => {
            return state.windowInsets.height > state.windowInsets.width;
        },
        isAdmin: state => {
            return state.authorization && state.authorization.group_id === 1;
        },
        getUserData: state => state.userData,
    },
    mutations: {
        SET_AUTHORIZATION(state, value) {
            state.authorization = value;
        },
        SET_NAV_WIDTH(state, value) {
            state.navWidth = value;
        },
        SET_WINDOW_INSETS(state, value) {
            state.windowInsets = value;
        },
        SET_NAV_MENU_STATUS(state, value) {
            state.navMenuIsClosed = value;
        },
        SET_IS_IN_MOBILE(state, value) {
            state.isInMobile = value;
        },
        SET_IS_SHOWING_MENU_TOGGLE_BTN(state, value) {
            state.isShowingMenuToggleBtn = value;
        },
        setUserData(state, userData) {
            state.userData = userData;
        },
    },
    actions: {
        saveUserData({ commit }, userData) {
            commit('setUserData', userData);
        },
    },
    computed: {
        ...mapState({
            userId: state => state.user.userId,
            username: state => state.user.userName,
            password: state => state.user.password
        })
    },
    created() {
        // 访问 this.userId 来获取 userId
        console.log('当前用户的 userId:', this.userId);
    }
});

export default store;
