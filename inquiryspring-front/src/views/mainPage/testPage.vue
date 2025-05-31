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
            <el-menu-item @click="gotoChat" index="2" style="border-radius: 8px; margin: 0 8px; width: calc(100% - 16px)">
                <i class="el-icon-chat-dot-round"></i>
                <span>智能答疑</span>
            </el-menu-item>
            <el-menu-item @click="gotoSummarize" index="3" style="border-radius: 8px; margin: 0 8px; width: calc(100% - 16px)">
                <i class="el-icon-chat-dot-round"></i>
                <span>智慧总结</span>
            </el-menu-item>
            <el-menu-item index="1" style="border-radius: 8px; margin: 0 8px; width: calc(100% - 16px); background: linear-gradient(135deg, #5a4a3a 0%, #3a2e24 100%); color: white; box-shadow: 0 2px 8px rgba(90, 74, 58, 0.3)">
                <i class="el-icon-edit" style="color: white"></i>
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
            <div class="content-container" style="flex: 1; display: flex; flex-direction: column; gap: 30px;">
                <el-col style="padding: 30px; background: rgba(255,255,255,0.9); border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); display: flex; gap: 10px;">
                    <div style="flex: 1; padding: 10px;">
                        <h3 style="margin-bottom: 15px; display: flex; align-items: center; gap: 5px;">
                            上传文件
                            <el-tooltip content="将根据上传的学习材料生成测试题目" placement="right">
                                <i class="el-icon-question" style="color: #8b7355; font-size: 16px;"></i>
                            </el-tooltip>
                        </h3>
                        <el-upload
                        class="upload-demo"
                        drag
                        action="/api/fileUpload/"
                        multiple>
                        <i class="el-icon-upload" style="color: #8b7355;"></i>
                        <div class="el-upload__text" style="color: #5a4a3a;">将文件拖到此处，或<em style="color: #8b7355;">点击上传</em></div>
                        <div class="el-upload__tip" slot="tip" style="color: #8b7355;">支持word,pdf格式</div>
                        </el-upload>
                    </div>
                    <div style="flex: 1; padding: 15px;">
                        <h3 style="margin-bottom: 15px; display: flex; align-items: center; gap: 5px;">
                            测试设置
                            <el-tooltip content="个性化生成你所需要的测试题目" placement="right">
                                <i class="el-icon-question" style="color: #8b7355; font-size: 16px;"></i>
                            </el-tooltip>
                        </h3>
                        <el-form ref="testReq" :model="testReq" label-width="80px">
                            <el-form-item label="题目数量">
                                <!-- <el-input type="text" maxlength="2" v-model="testReq.num"></el-input> -->
                                 <div class="block">
                                    <el-slider
                                    v-model="testReq.num"
                                    show-input>
                                    </el-slider>
                                </div>
                            </el-form-item>
                            <el-form-item label="题目类型">
                                <el-checkbox-group v-model="testReq.type">
                                <el-checkbox label="单选题" name="type"></el-checkbox>
                                <el-checkbox label="多选题" name="type"></el-checkbox>
                                <el-checkbox label="判断题" name="type"></el-checkbox>
                                <el-checkbox label="填空题" name="type"></el-checkbox>
                                </el-checkbox-group>
                            </el-form-item>
                            <el-form-item label="题目难度">
                                <el-radio-group v-model="testReq.level">
                                <el-radio label="简单"></el-radio>
                                <el-radio label="中等"></el-radio>
                                <el-radio label="困难"></el-radio>
                                </el-radio-group>
                            </el-form-item>
                            <el-form-item label="其他要求">
                                <el-input type="textarea" v-model="testReq.desc"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <v-btn @click="generateTest" color="#8b7355" style="color: white;">
                                    立即生成
                                </v-btn>
                            </el-form-item>
                        </el-form>
                    </div>
                </el-col>
                <el-col v-show="testVisible" style="padding: 20px; background: rgba(255,255,255,0.9); border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; justify-content: center; gap: 15px; margin-bottom: 20px;">
                        <v-btn @click="all" color="#8b7355" style="color: white;">
                            显示全部
                        </v-btn>
                        <v-btn @click="none" color="#e8dfc8" style="color: #5a4a3a;">
                            收起
                        </v-btn>
                    </div>

                    <v-expansion-panels
                    v-model="panel"
                    multiple
                    >
                    <v-expansion-panel
                        v-for="(item,i) in items"
                        :key="i"
                        style="margin-bottom: 10px; border: 1px solid rgba(139, 115, 85, 0.1); will-change: height;"
                    >
                        <v-expansion-panel-header 
                            expand-icon="mdi-menu-down" 
                            style="color: #5a4a3a; font-weight: 500;"
                            :class="{'v-expansion-panel-header--active': panel.includes(i)}"
                        >
                            题目 {{ item }}
                        </v-expansion-panel-header>
                        <v-expansion-panel-content 
                            style="color: #5a4a3a; line-height: 1.6; padding: 15px;"
                            v-if="panel.includes(i)"
                        >
                        <el-row>
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                        </el-row>
                        <el-row>
                            <v-text-field label="输入答案"></v-text-field>
                        </el-row>
                        
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                    </v-expansion-panels>
                    <v-btn @click="submitAns" color="#8b7355" style="color: white;">
                        提交答案
                    </v-btn>
                </el-col>
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
        box-shadow: 0 2px 8px rgba(90, 74, 58, 0.3) !important;
        transform: translateY(-1px);
    }
    
    .el-menu-item.is-active i {
        color: white !important;
    }
</style>

<script>
export default {
    data() {
        return {
            panel: [],
            items: 0,
            testVisible:false,
            testReq:{
                num:"",
                type:[],
                level:"",
                desc:""
            }
        }
    },
    methods: {
        gotoChat() {
            this.$router.push({ path: '/chat' });
        },
        gotoSummarize() {
            this.$router.push({ path: '/summarize' });
        },
        gotoPrj(){
            this.$router.push({ path: '/project' });
        },
        all () {
            this.panel = [...Array(this.items).keys()].map((k, i) => i)
        },
        // Reset the panel
        none () {
            this.panel = []
        },
        generateTest(){
            window.alert(JSON.stringify(this.testReq))
            this.items=this.testReq.num
            if(this.items>0){
                this.testVisible=true

            }
        },
        submitAns(){
            window.alert("提交成功")
        }
    }
};
</script>