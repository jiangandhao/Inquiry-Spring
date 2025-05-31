<template>
    <el-container style="height: 100vh; background: linear-gradient(135deg, #f5f1e8 0%, #f0e6d2 100%)">
    <el-aside width="240px" style="background: linear-gradient(to bottom, #e8dfc8, #d8cfb8); border-right: 1px solid #d4c9a8; border-radius: 0 12px 12px 0; box-shadow: 2px 0 10px rgba(0,0,0,0.1)">
        <el-row :gutter="20">
            <div style="color: #5a4a3a; padding: 15px; font-size: 18px; font-weight: bold; display: flex; flex-direction: column; align-items: center;">
                <div>
                    <i class="el-icon-connection" style="margin-right: 8px; color: #8b7355"></i>
                    <span>问泉-Inquiry Spring</span>
                </div>
                <div style="margin-top: 20px;">{{ this.$store.getters.getSelectedPrjName}}</div>
            </div>   
        </el-row>
        <el-menu 
            background-color="#e8dfc8"
            text-color="#5a4a3a"
            active-text-color="#ffffff"
            :default-active="'1'">
            <el-menu-item index="1" style="border-radius: 8px; margin: 0 8px; width: calc(100% - 16px); background: linear-gradient(135deg, #5a4a3a 0%, #3a2e24 100%); color: white; box-shadow: 0 2px 8px rgba(90, 74, 58, 0.3)">
                <i class="el-icon-chat-dot-round" style="color: white"></i>
                <span>智能答疑</span>
            </el-menu-item>
            <el-menu-item @click="gotoSummarize" index="2" style="border-radius: 8px; margin: 0 8px; width: calc(100% - 16px)">
                <i class="el-icon-notebook-2"></i>
                <span>智慧总结</span>
            </el-menu-item>
            <el-menu-item @click="gotoTest" index="3" style="border-radius: 8px; margin: 0 8px; width: calc(100% - 16px)">
                <i class="el-icon-edit"></i>
                <span>生成小测</span>
            </el-menu-item>
            <el-menu-item @click="gotoPrj" style="border-radius: 8px; margin: 8px; width: calc(100% - 16px); transition: all 0.3s">
                <i class="el-icon-folder-add" style="color: #8b7355"></i>
                <span>管理学习项目</span>
            </el-menu-item>
        </el-menu>
    </el-aside>
    
    <el-container>
        <el-main style="padding: 20px; display: flex; flex-direction: column; height: 100%; background-color: rgba(255,255,255,0.7); border-radius: 16px; margin: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border: 1px solid rgba(139, 115, 85, 0.1)">
            <div class="chat-container">
                <div class="message-list">
                    <div 
                        v-for="(message, index) in messages" 
                        :key="index" 
                        :class="['message-bubble', message.isUser ? 'user-message' : 'ai-message']">
                        <div class="message-content">{{ message.text }}</div>
                        <div class="message-time">{{ formatTime(message.timestamp) }}</div>
                    </div>
                </div>
                <div class="input-area" style="display: flex; gap: 10px; align-items: center;">
                    <el-input 
                        type="textarea" 
                        :rows="1" 
                        placeholder="输入你的问题..."
                        v-model="inputMessage"
                        @keyup.enter.native="sendMessage"
                        resize="none"
                        style="flex: 1; border-radius: 24px; padding: 12px 20px;">
                    </el-input>
                    <el-button 
                        type="primary" 
                        style="background: linear-gradient(135deg, #8b7355 0%, #a0866b 100%);
                               border: none;
                               border-radius: 24px;
                               padding: 12px 24px;
                               font-weight: 500;
                               letter-spacing: 1px;
                               box-shadow: 0 2px 6px rgba(139, 115, 85, 0.3);
                               transition: all 0.3s ease;
                               height: 48px;"
                        @click="sendMessage"
                        :disabled="!inputMessage.trim()"
                        class="send-button">
                        <i class="el-icon-s-promotion" style="margin-right: 6px"></i>
                        发送
                    </el-button>
                </div>
            </div>
        </el-main>
    </el-container>
    </el-container>
</template>

<style>
    .el-header {
        background-color: #B3C0D1;
        color: #333;
        line-height: 60px;
    }
    
    .el-aside {
        color: #333;
    }
    
    .el-menu-item {
        transition: all 0.3s ease;
    }
    
    .el-menu-item:hover {
        background-color: #d4c9a8;
    }
    
    .el-menu-item.is-active {
        background: linear-gradient(135deg, #a0866b 0%, #d4b999 100%) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(139, 115, 85, 0.3) !important;
        transform: translateY(-1px);
    }
    
    .el-menu-item.is-active i {
        color: white !important;
    }
    
    .chat-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        padding: 25px;
        background-color: rgba(255,255,255,0.7);
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(139, 115, 85, 0.1);
    }
    
    .message-list {
        flex: 1;
        overflow-y: auto;
        margin-bottom: 20px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 18px;
        background-color: rgba(255,255,255,0.5);
        border-radius: 12px;
        scrollbar-width: thin;
        scrollbar-color: #8b7355 #f0e6d2;
    }
    
    .message-list::-webkit-scrollbar {
        width: 6px;
    }
    
    .message-list::-webkit-scrollbar-thumb {
        background-color: #8b7355;
        border-radius: 3px;
    }
    
    .message-list::-webkit-scrollbar-track {
        background-color: #f0e6d2;
    }
    
    .message-bubble {
        max-width: 80%;
        padding: 14px 18px;
        border-radius: 14px;
        position: relative;
        word-break: break-word;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        font-family: 'Georgia', serif;
        transition: all 0.3s ease;
    }
    
    .message-bubble:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .user-message {
        align-self: flex-end;
        background: linear-gradient(135deg, #e8d5c0 0%, #f5e1c8 100%);
        color: #5a4a3a;
        margin-left: 20%;
    }
    
    .ai-message {
        align-self: flex-start;
        background: linear-gradient(135deg, #e8dfc8 0%, #f5f1e8 100%);
        color: #5a4a3a;
        margin-right: 20%;
        border: 1px solid rgba(139, 115, 85, 0.2);
    }
    
    .message-content {
        margin-bottom: 5px;
        line-height: 1.6;
        font-size: 15px;
    }
    
    .message-time {
        font-size: 12px;
        color: #8b7355;
        text-align: right;
    }
    
    .input-area {
        margin-bottom: 20px;
    }
    
    .el-textarea__inner {
        background-color: #fffdf9;
        border-color: #d4c9a8;
        color: #5a4a3a;
        font-family: 'Georgia', serif;
        border-radius: 24px !important;
        padding: 12px 20px !important;
        line-height: 1.6;
        min-height: 48px !important;
    }

    /* 发送按钮悬浮效果 */
    .send-button:not(:disabled):hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(139, 115, 85, 0.4);
        background: linear-gradient(135deg, #9d8266 0%, #b4967a 100%);
    }
    
    .send-button:not(:disabled):active {
        transform: scale(0.98);
    }
</style>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            url:this.HOST+'/chat/',
            inputMessage: '',
            messages: [],
            form:{
                message:'',
                timestamp:''
            }
        }
    },
    methods: {
        sendMessage() {
            if (this.inputMessage.trim() === '') return;
            this.form.message=this.inputMessage;
            this.form.timestamp=new Date()

            //发送消息到后端API
            axios.post(this.url,this.form).then(response=>{
                console.log(response.data.message);
            })
            .catch(error=>{
                this.$message.error('发送失败：'+error.message);
            })

            
            // 添加用户消息
            this.messages.push({
                text: this.inputMessage,
                isUser: true,
                timestamp: this.form.timestamp
            });
            
            // 清空输入框
            this.inputMessage = '';
            
            // 自动滚动到底部
            this.$nextTick(() => {
                const container = document.querySelector('.message-list');
                container.scrollTop = container.scrollHeight;
            });
            
            // TODO: 这里添加API调用获取AI回复的逻辑
            // 模拟AI回复
            setTimeout(() => {
                axios.get(this.url).then(response => {
                    console.log(response.data.AIMessage);
                    this.messages.push({
                    text: response.data.AIMessage,
                    isUser: false,
                    timestamp: new Date()
                });
                })
                .catch(error => {
                    this.$message.error('获取AI回复失败:' + error.message);
                });
                
                // 再次自动滚动
                this.$nextTick(() => {
                    const container = document.querySelector('.message-list');
                    container.scrollTop = container.scrollHeight;
                });
            }, 1000);
        },
        formatTime(date) {
            return `${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`;
        },
        gotoSummarize() {
            this.$router.push({ path: '/summarize' });
        },
        gotoTest() {
            this.$router.push({ path: '/test' });
        },
        gotoPrj(){
            this.$router.push({ path: '/project' });
        }
    }
};
</script>