<template>
    <div @click="toMainPage">进入</div>
</template>

<script>
    export default {
        methods: {
            toMainPage() {
                this.$router.push('/chat')
            }
        }
    }
</script>