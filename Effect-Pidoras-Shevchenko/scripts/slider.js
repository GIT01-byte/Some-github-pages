const slider = document.querySelector("#slider");
const sliderItems = Array.from(slider.children);
const btnPrev = document.querySelector("#btnPrev");
const btnNext = document.querySelector("#btnNext");

sliderItems.forEach(function (slide, index) {
  console.log(slide);

  // Скрываем все слайды кроме первого
  if (index !== 0) slide.classList.add("hidden");

  // Добавляем индексы
  slide.dataset.index = index;

  // Добавляем data атрибут active для первого слайда / активного слайда
  sliderItems[0].setAttribute("data-active", "");
});

btnNext.onclick = function () {
  console.log("Next Slide");

  showNextSlide("next");
};

btnPrev.onclick = function () {
  console.log("Prev Slide");

  showNextSlide("prev");
};

function showNextSlide(direction) {
  // Скрываем текущий слайд
  const currentSlide = slider.querySelector("[data-active]");
  const currentSlideIndex = +currentSlide.dataset.index;
  currentSlide.classList.add("hidden");
  currentSlide.removeAttribute("data-active");

  // Показываем след. слайд в зависимости от направления движения
  let nextSlideIndex;
  if (direction === "next") {
    nextSlideIndex =
      currentSlideIndex + 1 === sliderItems.length ? 0 : currentSlideIndex + 1;
  } else if (direction === "prev") {
    nextSlideIndex =
      currentSlideIndex === 0 ? sliderItems.length - 1 : currentSlideIndex - 1;
  }

  // Показываем след. слайд
  const nextSlide = slider.querySelector(`[data-index="${nextSlideIndex}"]`);
  nextSlide.classList.remove("hidden");
  nextSlide.setAttribute("data-active", "");
}
