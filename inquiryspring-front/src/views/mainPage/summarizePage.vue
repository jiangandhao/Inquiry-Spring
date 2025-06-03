<template>
    <el-container style="height: 100vh; background: linear-gradient(135deg, #f5f1e8 0%, #f0e6d2 100%)">
    <el-aside width="240px" style="background: linear-gradient(to bottom, #e8dfc8, #d8cfb8); border-right: 1px solid #d4c9a8; border-radius: 0 12px 12px 0; box-shadow: 2px 0 10px rgba(0,0,0,0.1); overflow-x: hidden">
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
            :default-active="'1'"
            style="overflow-x: hidden">
            <el-menu-item @click="gotoChat" index="2" style="border-radius: 8px; margin: 0 8px; width: calc(100% - 16px)">
                <i class="el-icon-chat-dot-round"></i>
                <span>智能答疑</span>
            </el-menu-item>
            <el-menu-item index="1" style="border-radius: 8px; margin: 0 8px; width: calc(100% - 16px); background: linear-gradient(135deg, #5a4a3a 0%, #3a2e24 100%); color: white; box-shadow: 0 2px 8px rgba(90, 74, 58, 0.3)">
                <i class="el-icon-notebook-2" style="color: white"></i>
                <span>智慧总结</span>
            </el-menu-item>
            <el-menu-item @click="gotoTest" index="3" style="border-radius: 8px; margin: 8px; width: calc(100% - 16px); transition: all 0.3s">
                <i class="el-icon-edit" style="color: #8b7355"></i>
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
            <div class="content-container" style="margin: 16px; padding: 0; background: transparent; box-shadow: none; border: none">
                <el-row :gutter="20" style="height: 100%">
                    <el-col :span="8" style="padding: 16px;">
                        <div style="height: 100%; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.05); display: flex; flex-direction: column;">
                            <h3 style="margin-bottom: 16px; color: #5a4a3a; display: flex; align-items: center; gap: 8px;">
                                上传文件
                                <el-tooltip content="上传的学习材料或学习笔记，生成总结" placement="right">
                                    <i class="el-icon-question" style="color: #8b7355; font-size: 16px;"></i>
                                </el-tooltip>
                            </h3>
                            <div style="flex: 1; display: flex; flex-direction: column;">
                                <el-upload
                                class="upload-demo"
                                drag
                                :action=this.url
                                multiple
                                :on-success="handleUploadSuccess"
                                :before-upload="beforeUpload"
                                style="flex: 1; display: flex; flex-direction: column;">
                                <i class="el-icon-upload" style="color: #8b7355; font-size: 48px; margin-bottom: 16px;"></i>
                                <div class="el-upload__text" style="color: #5a4a3a; font-size: 14px;">将文件拖到此处，或<em style="color: #8b7355;">点击上传</em></div>
                                <div class="el-upload__tip" slot="tip" style="color: #8b7355; margin-top: 16px;">支持word,pdf格式，大小不超过10MB</div>
                                </el-upload>
                                <v-btn @click="generateSummary" color="#8b7355" style="color: white; margin-top: 20px; align-self: flex-end;">
                                    立即生成
                                </v-btn>
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="16" style="padding: 16px;">
                        <div style="height: 100%; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.05); display: flex; flex-direction: column;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                                <h3 style="color: #5a4a3a;">总结内容</h3>
                                <v-btn @click="output" color="#8b7355" style="color: white;">
                                    导出
                                </v-btn>
                            </div>
                            <v-textarea
                            name="input-7-1"
                            filled
                            auto-grow
                            v-model="summarizeMsg"
                            style="flex: 1;"
                            ></v-textarea>
                        </div>
                    </el-col>
                </el-row>
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
    
    .content-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        padding: 25px;
        background-color: rgba(255,255,255,0.7);
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(139, 115, 85, 0.1);
    }
</style>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            summarizeMsg:"问渠哪得清如许，为有源头活水来",
            url:this.HOST+'/summarize/',
        }
    },
    methods: {
        gotoChat() {
            this.$router.push({ path: '/chat' });
        },
        gotoTest() {
            this.$router.push({ path: '/test' });
        },
        output(){
            window.alert(this.summarizeMsg);
        },
        gotoPrj(){
            this.$router.push({ path: '/project' });
        },

        // 上传文件前的校验
        beforeUpload(file) {
        const isLt10M = file.size / 1024 / 1024 < 10;
        if (!isLt10M) {
            this.$message.error('上传文件大小不能超过10MB!');
        }
        return isLt10M;
        },

        // 文件上传成功处理
        handleUploadSuccess(response, file) {
            console.log(response.data)
            this.$message.success(`${file.name} 上传成功`);
        },

        generateSummary(){
            axios.get(this.url).then((response)=>{
                this.summarizeMsg=response.data.AIMessage;
            })
            .catch(error => {
                this.$message.error('获取AI回复失败:' + error.message);
            });
        }
    }
};
</script>