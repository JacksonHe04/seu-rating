<template>
  <slot name="secondTitleDiv">
    <div class="musicians_section layout_padding">
      <div class="container" style="margin-top: -100px">
        <h1 class="musicians_text">
          Discover Good<br />
          <slot name="secondTitle"> Albums </slot>
        </h1>
      </div>
    </div>
  </slot>
</template>