<template>
  <footer class="footer_section layout_padding">
    <!-- 页脚部分的布局，为用户提供建议功能 -->
    <!--      <div class="footer_section layout_padding">-->
    <!-- 容器，包含建议表单的所有元素 -->
    <div class="container">
      <!-- 建议标题 -->
      <h1 class="advice_title">给我们提建议</h1>
      <!-- 对建议功能的简要描述 -->
      <p class="advice_text">
        如果你对我们的项目有任何建议，欢迎在这里填写，我们会尽快处理。
      </p>
      <!-- 输入建议的表单 -->
      <div class="box_main_2">
        <!--suppress HtmlFormInputWithoutLabel, HtmlFormInputWithoutLabel -->
        <textarea
            type=""
            class="advice_bt"
            placeholder="填写你的建议"
            name=""
        ></textarea>
      </div>
      <!-- 提交按钮，引导用户进行提交操作 -->
      <button class="submit_bt"><a href="#">提交</a></button>
    </div>
    <!--      </div>-->

    <!-- 版权和信息区域 -->
    <div class="copyright_section">
      <!-- 使用.container类创建一个容器 -->
      <div class="container">
        <!-- 使用.row类创建一个行 -->
        <div class="row">
          <!-- 使用.col-md-6类创建一个占6列的列 -->
          <div class="col-md-6">
            <!-- 版权信息文本，并指向仓库链接 -->
            <p class="copyright_text">
              &copy; 2024 SEU Music Rating, all rights reserved
              <a
                  href="https://gitee.com/jacksonhe04/BDTrueValueRecSys"
                  class="authors_text"
              >蒋妙 何锦诚 吴锦承</a
              >
            </p>
          </div>
          <!-- 另一个占6列的列，用于展示Cookies、隐私和条款信息 -->
          <div class="col-md-6">
            <!-- Cookies、隐私和条款文本 -->
            <p class="cookies_text">Cookies, Privacy and Terms</p>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>