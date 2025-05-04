<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="bg-white p-4 mb-6 rounded border border-gray-200">
                <div class="my-4">
                    <ul>
                        <li class="mb-4">
                            <div class="flex justify-between items-center space-x-2">
                                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjYaK0N_g8erthyNgnhxn8dse9ImHEXm6gpw&s" class="rounded-full h-10 w-10"/>
                                <p class="text-xs truncate ... font-semibold">Name of the user</p>
                                <p class="text-xs text-gray-500">18 minutes ago</p>
                            </div>
                        </li>
                        <li class="mb-4">
                            <div class="flex justify-between items-center space-x-2">
                                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjYaK0N_g8erthyNgnhxn8dse9ImHEXm6gpw&s" class="rounded-full h-10 w-10"/>
                                <p class="text-xs truncate ... font-semibold">Name of the user</p>
                                <p class="text-xs text-gray-500">18 minutes ago</p>
                            </div>
                        </li>
                        <li class="mb-4">
                            <div class="flex justify-between items-center space-x-2">
                                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjYaK0N_g8erthyNgnhxn8dse9ImHEXm6gpw&s" class="rounded-full h-10 w-10"/>
                                <p class="truncate ... text-xs font-semibold">Name of the user</p>
                                <p class="text-xs text-gray-500">18 minutes ago</p>
                            </div>
                        </li>
                        <li class="mb-4">
                            <div class="flex justify-between items-center space-x-2">
                                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjYaK0N_g8erthyNgnhxn8dse9ImHEXm6gpw&s" class="rounded-full h-10 w-10"/>
                                <p class="truncate ... text-xs font-semibold">Name of the user</p>
                                <p class="text-xs text-gray-500">18 minutes ago</p>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>  
        <div class="main-right col-span-3">
            <div class="bg-white border border-gray-200 rounded-lg">
                <div class="flex flex-col flex-grow p-4">
                    <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
                        <div>
                            <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Nostrum aliquam voluptates commodi minus? Voluptates, iure esse? Odio deserunt perspiciatis numquam id eveniet aut. Consequuntur repellat doloribus cumque quae reprehenderit sunt?</p>
                            </div>
                            <span class="text-xs text-gray-500 leading-none">2 mins ago</span>
                        </div>
                        <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjYaK0N_g8erthyNgnhxn8dse9ImHEXm6gpw&s" class="rounded-full w-[40px]"/>
                        </div>
                    </div>
                    <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
                        <div>
                            <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                                <p>Lorem ipsum dolor sit amet  </p>
                            </div>
                            <span class="text-xs text-gray-500 leading-none">2 mins ago</span>
                        </div>
                        <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjYaK0N_g8erthyNgnhxn8dse9ImHEXm6gpw&s" class="rounded-full w-[40px]"/>
                        </div>
                    </div>
                    <div class="flex w-full mt-2 space-x-3 max-w-md mr-auto">
                        <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjYaK0N_g8erthyNgnhxn8dse9ImHEXm6gpw&s" class="rounded-full w-[40px]"/>
                        </div>
                        <div>
                            <div class="bg-gray-200 text-gray-800 p-3 rounded-r-lg rounded-bl-lg">
                                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Nostrum aliquam voluptates commodi minus? Voluptates, iure esse? Odio deserunt perspiciatis numquam id eveniet aut. Consequuntur repellat doloribus cumque quae reprehenderit sunt?</p>
                            </div>
                            <span class="text-xs text-gray-500 leading-none">2 mins ago</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bg-white border border-gray-200 rounded-lg">
                <div class="flex justify between p-4">
                    <div class="w-full">
                        <textarea class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Write your message"></textarea>
                    </div>
                    <div>
                        <button class="px-4 mx-3 py-2 bg-purple-500 hover:bg-purple-700 rounded-lg text-white">Send</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>