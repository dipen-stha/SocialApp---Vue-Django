<template>
    <ContentLayout :title="layout.title" :actions="layout.actions">
        <template #header>
            <div class="flex">
                <div>
                    <span class="text-3xl">Users</span>
                </div>
            </div>
        </template>
        <template #body>
            <div class="p-3">
                <table class="w-full ">
                    <thead class="">
                        <tr>
                            <th class="border border-gray-200 px-2 py-1">S.N.</th>
                            <th class="border border-gray-200 px-2 py-1 w-[400px]">User</th>
                            <th class="border border-gray-200 px-2 py-1 w-[400px]">Email</th>
                            <th class="border border-gray-200 px-2 py-1">Status</th>
                            <th class="border border-gray-200 px-2 py-1 truncate">Last Logged In</th>
                            <th class="border border-gray-200 px-2 py-1">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="">

                    </tbody>
                </table>
            </div>
        </template>
    </ContentLayout>
</template>

<script setup>
import ContentLayout from '@/components/ContentLayout.vue';
import { useUserStore } from '@/stores/user/user';
import { onMounted, ref } from 'vue';

const layout = ref(
    {
        title: 'User',
        actions: [
            {
                title: 'Create',
                emit: 'onCreate',
            },
            {
                title: 'View',
                emit: 'onView'
            }
        ]
    },
)

const userStore = useUserStore();

onMounted(() => {
    userStore.fetch
})
</script>