import router from "@/router";
import { useUserStore } from "@/stores/user/user";

const initRouter = (app) => {
    const userStore = useUserStore();
    router.beforeEach(async (to, from, next) => {
        try{
            await userStore.fetchSelfDetail();
        } catch (error){
            console.log("Error fetching user detail", error)
        }
        if (to.name === 'login'){
            if(userStore.isAuthenticated){
                if(userStore.self.is_verified){
                    next({name: 'feed'})
                } else {
                    next({ name: 'unverified'})
                }
            } else{
                next();
            }
        } else if(to.name === 'unverified'){
            if(userStore.isAuthenticated){
                next();
            } else{
                next({name: 'login'})
            }
        } else if (to.name === 'verify'){
            next();
        } 
        else {
            if (to.meta.requiresAuth) {
                if (userStore.isAuthenticated){
                    if(userStore.self.is_verified && to.name === 'verify'){
                    next();
                } else {
                    next({ name: 'unverified'})
                }
                } else {
                    next({ name: 'login'});
                }
            } else {
                next();
            }
        }
    });
    app.use(router);
}

export default initRouter;