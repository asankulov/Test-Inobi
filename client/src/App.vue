<template>
  <v-app>
    <v-toolbar dark color="primary">
      <v-toolbar-title class="white--text">{{ title }}</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-content>
      <v-container grid-list-md>
        <v-layout align-center row justify-start full-height>
          <v-alert
            v-model="alert"
            dismissible
            type="error"
          >
            Что-то пошло не так!
          </v-alert>
          <v-alert
            v-model="formHasErrors"
            dismissible
            type="error"
          >
            Заполните поля корректными данными!
          </v-alert>
        </v-layout>
        <v-layout align-center row justify-start>
          <v-flex xs6 class="text-xs-center text-sm-center text-md-center text-lg-center">
            <v-text-field label="Выбрать Картинку" @click='pickFile' v-model='imageName'
                          prepend-icon='attach_file' readonly></v-text-field>
            <input
              type="file"
              style="display: none"
              ref="image"
              accept="image/jpeg, image/png"
              @change="onFilePicked"
            >
          </v-flex>
        </v-layout>
        <v-layout v-if="this.imageFile !== ''" align-start row justify-start>
          <v-flex xs3>
            <v-text-field label="Горизонтальное соотношение"
                          v-model="horizontalRatio"
                          outline
                          clearable
                          mask="########"
                          validate-on-blur
                          ref="horizontalRatio"
                          :rules="[
                          () => !!horizontalRatio || 'Это поле обязательно',
                          () => !!horizontalRatio && horizontalRatio > 0 || 'Значение должно быть больше 0',
                          () => !!horizontalRatio && horizontalRatio <= originalSize.w || 'Значение не должно быть больше оригинальной ширины'
                          ]"
            >
            </v-text-field>
          </v-flex>
          <v-flex xs3>
            <v-text-field label="Вертикальное соотношение"
                          v-model="verticalRatio"
                          outline
                          clearable
                          mask="########"
                          validate-on-blur
                          ref="verticalRatio"
                          :rules="[
                          () => !!verticalRatio || 'Это поле обязательно',
                          () => !!verticalRatio && verticalRatio > 0 || 'Значение должно быть больше 0',
                          () => !!verticalRatio && verticalRatio <= originalSize.h || 'Значение не должно быть больше оригинальной высоты'
                          ]"
            >
            </v-text-field>
          </v-flex>
          <v-flex xs3>
            <v-btn
              :loading="reactiveLoader"
              :disabled="reactiveLoader"
              color="primary"
              class="white--text"
              @click="upload"
              large
            >
              Поделить картинку
              <v-icon right dark>cloud_upload</v-icon>
            </v-btn>
          </v-flex>
        </v-layout>
        <v-layout v-if="resData !== null" align-center justify-center row>
          <v-list>
            <v-list-tile
              v-for="item in images"
              :key="item"
              avatar
            >
              <v-list-tile-content>
                <v-list-tile-title v-html="item"></v-list-tile-title>
              </v-list-tile-content>

              <v-list-tile-avatar>
                <img :alt="item" :src="`${proxyServer}/uploads/${dirname}/${item}`">
              </v-list-tile-avatar>


                <v-list-tile-action>
                  <a style="margin-right: inherit; text-decoration: none;" :href="`${proxyServer}/download/${dirname}/${item}`">
                    <v-icon color="primary">archive</v-icon>
                  </a>
                </v-list-tile-action>
            </v-list-tile>
          </v-list>
          <v-flex offset-xs1 xs2>
            <h2>ИЛИ</h2>
          </v-flex>
          <v-flex xs3>
            <v-btn
              block
              color="primary"
              class="white--text"
              :href="`${proxyServer}/download/${dirname}`"
            >
              Скачать все разом
              <v-icon right dark>archive</v-icon>
            </v-btn>
            <v-btn
              block
              color="error"
              class="white--text"
              @click="clear"
            >
              Очистить
              <v-icon right dark>autorenew</v-icon>
            </v-btn>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
  import axios from 'axios';

  function getImageSize(file) {
    return new Promise(((resolve, reject) => {
      if (file) {
        let img = new Image();
        img.src = URL.createObjectURL(file);
        img.onload = () => {
          let width = img.naturalWidth;
          let  height = img.naturalHeight;
          URL.revokeObjectURL(img.src);
          resolve({height, width})
        };
      } else {
        reject('File Is Not Defined!')
      }
    }))
  }

  export default {
    name: 'App',
    data: () => ({
      proxyServer: 'http://localhost:5000',
      title: "Работа с картинками 😎😎",
      dialog: false,
      imageName: '',
      imageUrl: '',
      imageFile: '',
      loader: null,
      loading: false,
      horizontalRatio: 3,
      verticalRatio: 3,
      originalSize: {
        w: 0,
        h: 0
      },
      errorMessages: '',
      formHasErrors: false,
      alert: false,
      resData: null
    }),
    computed: {
      form () {
        return {
          horizontalRatio: this.horizontalRatio,
          verticalRatio: this.verticalRatio
        }
      },
      reactiveLoader() {
        return this.loader
      },
      images() {
        return this.resData.files.sort()
      },
      dirname() {
        return this.resData.dirname
      }
    },
    methods: {
      pickFile() {
        this.$refs.image.click()
      },
      onFilePicked(e) {
        const files = e.target.files;
        if (files[0] !== undefined) {
          this.imageName = files[0].name;
          if (this.imageName.lastIndexOf('.') <= 0) {
            return
          }
          const fr = new FileReader();
          fr.readAsDataURL(files[0]);
          fr.addEventListener('load', () => {
            this.imageUrl = fr.result;
            this.imageFile = files[0];
            getImageSize(this.imageFile)
              .then(({width, height}) => {
                this.originalSize.w = width;
                this.originalSize.h = height;
              })
              .catch(e => {
                console.log(e)
              })
          })
        } else {
          this.clear();
        }
      },
      upload() {
        this.validate();
        if(this.formHasErrors) {
          return
        }
        this.loader = true;
        const formData = new FormData();
        formData.append('image', this.imageFile);
        axios.post(`${this.proxyServer}/split/${this.horizontalRatio}x${this.verticalRatio}`, formData)
          .then(res => {
            this.resData = Object.assign({}, res.data);
            this.loader = false;
            this.imageFile = ''
          })
          .catch(e => {
            console.log(e);
            this.alert = true;
            this.loader = false;
          })
      },
      validate() {
        this.formHasErrors = false;
        Object.keys(this.form).forEach(f => {
          if (!this.form[f] || this.form[f] <= 0) {
            this.formHasErrors = true;
          }
          this.$refs[f].validate(true)
        });
        if(this.form.horizontalRatio > this.originalSize.h || this.form.verticalRatio > this.originalSize.w) {
          this.formHasErrors = true;
        }
      },
      clear() {
        this.resData = null;
        this.imageName = '';
        this.imageFile = '';
        this.imageUrl = '';
      }
    }
  }
</script>
<style>
  .custom-loader {
    animation: loader 1s infinite;
    display: flex;
  }
  @-moz-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @-webkit-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @-o-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
</style>
