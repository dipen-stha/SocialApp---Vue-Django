<template>
    <div class="flex flex-col h-screen w-full admin-text">
        <header class="h-16 admin-border p-4">
            <slot name="header"></slot>
        </header>
        <main class="flex-1 overflow-auto p-4">
            <slot name="body"></slot>
        </main>
        <footer class="h-12 admin-border">
      <slot name="footer"></slot>
    </footer>
    </div>
</template>