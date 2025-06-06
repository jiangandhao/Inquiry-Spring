<!-- <template>
  <div>
    <div class="markdown-container" v-html="markMessage(md)"></div>
    <div>
      <v-card>
        <v-container fluid>
          <v-row>
            <v-col cols="12">
              <v-combobox
                v-model="value"
                :items="items"
                label="Default"
              ></v-combobox>
            </v-col>
            <v-col cols="12">
              <v-combobox
                v-model="value"
                :items="items"
                density="comfortable"
                label="Comfortable"
              ></v-combobox>
            </v-col>
            <v-col cols="12">
              <v-combobox
                v-model="value"
                :items="items"
                density="compact"
                label="Compact"
              ></v-combobox>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </div>
  </div>
  
</template>

<style scoped>
.markdown-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.6;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.markdown-container >>> h1, 
.markdown-container >>> h2, 
.markdown-container >>> h3 {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
}

.markdown-container >>> p {
  margin-bottom: 1em;
}

.markdown-container >>> pre {
  background: #f6f8fa;
  padding: 16px;
  border-radius: 6px;
  overflow: auto;
  margin: 1em 0;
}

.markdown-container >>> code {
  font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
}

.markdown-container >>> blockquote {
  border-left: 4px solid #8b7355;
  background: #f8f6f2;
  color: #6a5a3a;
  margin: 1em 0;
  padding: 0.7em 1.2em;
  border-radius: 4px;
  font-style: italic;
}
</style>
<script>
import { Marked } from 'marked'
import { markedHighlight } from "marked-highlight";
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';
import "highlight.js/styles/paraiso-light.css";

export default {
 data(){
   return {
      md:"# Hello, world!\n\nThis is a markdown file.\n\n```js\nconsole.log('Hello, world!');\n```\n\n> quote",

      messages: [], // 消息记录
      userInput: "你好", // 用户输入，默认一开始发一个“你好”
      pollingActive: false, // 是否正在长轮询
      isEnd: false, // 标记是否结束轮询
      currentAiMessageId: null, // 当前正在回复的 AI 消息的 ID
      userMsgData: {}, // 用户消息数据
    };
 },
//  computed: {
//    markdownToHtml(){
//      return marked(this.markdown);
//    }
//  },
 methods:{
  markMessage(message) {
      message=message.replaceAll('\\n','\n')
      // console.log('调用前'+message)
      const marked = new Marked(
        markedHighlight({
          pedantic: false,
          gfm: true, // 开启gfm
          breaks: true,
          smartLists: true,
          xhtml: true,
          async: false, // 如果是异步的，可以设置为 true
          langPrefix: 'hljs language-', // 可选：用于给代码块添加前缀
          emptyLangClass: 'no-lang', // 没有指定语言的代码块会添加这个类名
          highlight: (code) => {
                 return hljs.highlightAuto(code).value
          }
        })
      );
     let  markedMessage = marked.parse(message)
      // console.log('调用了'+markedMessage)
      return markedMessage
    },
 }
}
</script> -->

<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <v-combobox
          v-model="select"
          :items="items"
          label="Combobox"
          multiple
          outlined
          dense
        ></v-combobox>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    data () {
      return {
        select: ['Vuetify', 'Programming'],
        items: [
          'Programming',
          'Design',
          'Vue',
          'Vuetify',
        ],
      }
    },
  }
</script>
