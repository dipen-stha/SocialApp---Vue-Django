export function toggleBodyScroll (isDisabled) {
    const scrollWidth = window.innerWidth - document.documentElement.clientWidth;

    if (isDisabled) {
        document.body.style.overflow = "hidden";
        document.body.style.paddingRight = `${scrollWidth}`;
    } else {
        document.body.style.overflow = "";
        document.body.style.paddingRight = "";
    }
}