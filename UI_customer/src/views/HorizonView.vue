<template>
  <div class="horizon-app min-h-screen text-[#F8F8FF]">
    <main class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <Transition name="fade-slide" mode="out-in">
        <section v-if="stage === 'landing'" key="landing" class="rounded-3xl border border-white/20 bg-white/5 p-8 shadow-2xl backdrop-blur-xl md:p-14">
          <p class="mb-4 inline-block rounded-full border border-[#C9956C]/60 bg-[#C9956C]/15 px-4 py-1 text-sm tracking-wide text-[#E8C8A8]">
            HORIZON
          </p>
          <h1 class="text-4xl font-semibold leading-tight md:text-6xl">Your timeline. Your rules.</h1>
          <p class="mt-5 max-w-2xl text-lg text-[#F8F8FF]/80 md:text-xl">Plan your career and life together — with real data, zero pressure.</p>
          <button class="mt-10 rounded-xl bg-[#C9956C] px-8 py-3 text-base font-semibold text-[#0D0F1A] transition hover:translate-y-[-2px] hover:shadow-lg hover:shadow-[#C9956C]/30" @click="stage = 'quiz'">
            Find My Path
          </button>
        </section>

        <section v-else-if="stage === 'quiz'" key="quiz" class="mx-auto max-w-2xl rounded-3xl border border-white/20 bg-white/5 p-7 shadow-2xl backdrop-blur-xl md:p-10">
          <div class="mb-8 h-2 w-full overflow-hidden rounded-full bg-white/10">
            <div class="h-full bg-gradient-to-r from-[#A78BFA] to-[#C9956C] transition-all duration-500" :style="{ width: `${(quizStep / 5) * 100}%` }" />
          </div>

          <Transition name="fade-slide" mode="out-in">
            <div :key="quizStep">
              <div v-if="quizStep === 1">
                <h2 class="text-2xl font-semibold">How old are you?</h2>
                <p class="mt-2 text-[#F8F8FF]/70">Move the slider to your current age.</p>
                <div class="mt-8">
                  <input v-model.number="profile.age" type="range" min="22" max="40" class="h-2 w-full cursor-pointer accent-[#C9956C]" />
                  <p class="mt-4 text-center text-4xl font-semibold text-[#E8C8A8]">{{ profile.age }}</p>
                </div>
              </div>

              <div v-else-if="quizStep === 2">
                <h2 class="text-2xl font-semibold">What industry are you in?</h2>
                <select v-model="profile.industry" class="mt-8 w-full rounded-xl border border-white/25 bg-[#0D0F1A]/70 p-4 text-[#F8F8FF] focus:border-[#C9956C] focus:outline-none">
                  <option v-for="item in industries" :key="item" :value="item">{{ item }}</option>
                </select>
              </div>

              <div v-else-if="quizStep === 3">
                <h2 class="text-2xl font-semibold">What's your career goal?</h2>
                <div class="mt-6 grid gap-4">
                  <button
                    v-for="goal in goals"
                    :key="goal"
                    class="rounded-2xl border p-4 text-left transition"
                    :class="profile.goal === goal ? 'border-[#C9956C] bg-[#C9956C]/20' : 'border-white/20 bg-white/5 hover:border-[#A78BFA]'"
                    @click="profile.goal = goal"
                  >
                    {{ goal }}
                  </button>
                </div>
              </div>

              <div v-else-if="quizStep === 4">
                <h2 class="text-2xl font-semibold">What's your relationship status?</h2>
                <div class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
                  <button
                    v-for="status in relationshipOptions"
                    :key="status"
                    class="rounded-2xl border p-4 capitalize transition"
                    :class="profile.relationship === status ? 'border-[#C9956C] bg-[#C9956C]/20' : 'border-white/20 bg-white/5 hover:border-[#A78BFA]'"
                    @click="profile.relationship = status"
                  >
                    {{ status }}
                  </button>
                </div>
              </div>

              <div v-else>
                <h2 class="text-2xl font-semibold">How do you feel about family planning right now?</h2>
                <div class="mt-6 grid gap-4">
                  <button
                    v-for="intent in familyIntentions"
                    :key="intent"
                    class="rounded-2xl border p-4 text-left transition"
                    :class="profile.familyIntention === intent ? 'border-[#C9956C] bg-[#C9956C]/20' : 'border-white/20 bg-white/5 hover:border-[#A78BFA]'"
                    @click="profile.familyIntention = intent"
                  >
                    {{ intent }}
                  </button>
                </div>
              </div>
            </div>
          </Transition>

          <div class="mt-10 flex justify-between">
            <button class="rounded-xl border border-white/30 px-5 py-2" :disabled="quizStep === 1" @click="quizStep--">Back</button>
            <button class="rounded-xl bg-[#C9956C] px-5 py-2 font-semibold text-[#0D0F1A]" @click="nextQuizStep">
              {{ quizStep === 5 ? 'See Results' : 'Next' }}
            </button>
          </div>
        </section>

        <section v-else-if="stage === 'dashboard'" key="dashboard" class="space-y-6">
          <header class="flex flex-wrap items-center justify-between gap-4">
            <h2 class="text-3xl font-semibold">Your 3 Life Paths</h2>
            <button class="rounded-xl border border-white/30 px-4 py-2" @click="stage = 'quiz'">Edit Inputs</button>
          </header>

          <div class="grid gap-4 lg:grid-cols-3">
            <article
              v-for="path in paths"
              :key="path.id"
              class="rounded-2xl border border-white/20 bg-white/5 p-5 backdrop-blur-xl"
            >
              <h3 class="text-xl font-semibold">{{ path.emoji }} {{ path.name }}</h3>
              <p class="mt-3 text-sm text-[#F8F8FF]/75">{{ path.fertility }}% natural conception odds</p>
              <p class="mt-2 text-sm text-[#F8F8FF]/75">Projected income at 40: <span class="font-semibold text-[#E8C8A8]">${{ path.income.toLocaleString() }}</span></p>
              <p class="mt-2 text-sm">{{ path.tradeoff }}</p>
              <button class="mt-5 w-full rounded-lg bg-[#A78BFA] px-4 py-2 font-medium text-[#0D0F1A] transition hover:bg-[#c4b1ff]" @click="selectPath(path)">
                Choose This Path
              </button>
            </article>
          </div>

          <div class="rounded-2xl border border-white/20 bg-white/5 p-4 md:p-6">
            <h3 class="mb-4 text-lg font-semibold">Fertility vs Career Curve (Age 25–45)</h3>
            <svg viewBox="0 0 720 260" class="h-72 w-full">
              <polyline fill="none" stroke="#A78BFA" stroke-width="4" :points="fertilityPoints" />
              <polyline fill="none" stroke="#C9956C" stroke-width="4" :points="incomePoints" />
              <line x1="40" y1="20" x2="40" y2="220" stroke="#fff" stroke-opacity="0.35" />
              <line x1="40" y1="220" x2="680" y2="220" stroke="#fff" stroke-opacity="0.35" />
              <text x="48" y="30" fill="#F8F8FF" font-size="12">100</text>
              <text x="655" y="240" fill="#F8F8FF" font-size="12">45</text>
            </svg>
            <div class="mt-2 flex gap-6 text-sm">
              <span><span class="mr-2 inline-block h-2 w-2 rounded-full bg-[#A78BFA]" />Fertility Index</span>
              <span><span class="mr-2 inline-block h-2 w-2 rounded-full bg-[#C9956C]" />Income Index</span>
            </div>
          </div>

          <div class="rounded-2xl border border-white/20 bg-white/5 p-6">
            <h3 class="text-xl font-semibold">What-If Simulator</h3>
            <div class="mt-5 space-y-6">
              <div>
                <label class="mb-2 block">Delay career focus by <span class="font-semibold text-[#E8C8A8]">{{ simulation.delayYears }} years</span></label>
                <input v-model.number="simulation.delayYears" type="range" min="0" max="5" class="h-2 w-full accent-[#C9956C]" />
                <p class="mt-1 text-sm text-[#F8F8FF]/65">See how strategic pacing can shift both growth and optionality.</p>
              </div>
              <div>
                <label class="mb-2 block">Consider egg freezing at age <span class="font-semibold text-[#E8C8A8]">{{ simulation.eggFreezeAge }}</span></label>
                <input v-model.number="simulation.eggFreezeAge" type="range" min="25" max="35" class="h-2 w-full accent-[#A78BFA]" />
                <p class="mt-1 text-sm text-[#F8F8FF]/65">Information-first planning can preserve more flexibility for future decisions.</p>
              </div>
            </div>
          </div>
        </section>

        <section v-else key="action" class="relative overflow-hidden rounded-3xl border border-white/20 bg-white/10 p-8 text-center shadow-2xl md:p-14">
          <div class="pointer-events-none absolute inset-0">
            <span v-for="dot in confettiDots" :key="dot.id" class="confetti" :style="dot.style" />
          </div>
          <h2 class="text-3xl font-semibold md:text-5xl">Your First Step This Month</h2>
          <p class="mt-7 text-3xl font-bold text-[#E8C8A8]">{{ selectedPath?.firstStep }}</p>
          <p class="mt-3 text-[#F8F8FF]/75">It's just information, not a commitment.</p>
          <div class="mt-10 flex flex-wrap justify-center gap-3">
            <button class="rounded-lg bg-[#C9956C] px-5 py-2 font-semibold text-[#0D0F1A]">Save Path</button>
            <button class="rounded-lg border border-white/40 px-5 py-2">Share</button>
            <button class="rounded-lg border border-white/40 px-5 py-2">Explore resources</button>
          </div>
          <button class="mt-10 rounded-lg bg-[#A78BFA] px-6 py-2 font-semibold text-[#0D0F1A]" @click="stage = 'dashboard'">Back to Dashboard</button>
        </section>
      </Transition>
    </main>

    <button class="fixed bottom-6 right-6 rounded-full bg-[#C9956C] px-5 py-3 font-semibold text-[#0D0F1A] shadow-lg shadow-[#C9956C]/30" @click="chatOpen = !chatOpen">
      Ask Advisor
    </button>

    <Transition name="slide-up">
      <aside v-if="chatOpen" class="fixed bottom-24 right-6 z-20 w-[92vw] max-w-md rounded-2xl border border-white/20 bg-[#10142A]/95 p-4 shadow-2xl backdrop-blur-xl">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="font-semibold">AI Advisor</h3>
          <button class="text-sm text-[#F8F8FF]/70" @click="chatOpen = false">Close</button>
        </div>
        <div class="max-h-80 space-y-3 overflow-y-auto pr-1">
          <div v-for="msg in chatMessages" :key="msg.id" :class="msg.role === 'user' ? 'text-right' : ''">
            <p class="inline-block max-w-[90%] rounded-2xl px-3 py-2 text-sm" :class="msg.role === 'user' ? 'bg-[#C9956C] text-[#0D0F1A]' : 'bg-white/10 text-[#F8F8FF]'">
              {{ msg.text }}
            </p>
          </div>
        </div>
        <div class="mt-4 space-y-2">
          <button v-for="prompt in promptOptions" :key="prompt" class="w-full rounded-lg border border-white/25 px-3 py-2 text-left text-sm hover:border-[#A78BFA]" @click="sendPrompt(prompt)">
            {{ prompt }}
          </button>
        </div>
      </aside>
    </Transition>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';

const stage = ref('landing');
const quizStep = ref(1);
const chatOpen = ref(false);

const industries = ['Tech', 'Finance', 'Healthcare', 'Creative', 'Other'];
const goals = ['Make Partner/Executive', 'Build My Own Thing', 'Work-Life Balance'];
const relationshipOptions = ['single', 'partnered', 'married'];
const familyIntentions = ['Definitely want kids', 'Open to it', 'Unsure'];

const profile = ref({
  age: 28,
  industry: 'Tech',
  goal: goals[0],
  relationship: 'single',
  familyIntention: familyIntentions[1],
});

const simulation = ref({
  delayYears: 1,
  eggFreezeAge: 30,
});

const promptOptions = [
  "What's the difference between freezing eggs at 28 vs 32?",
  'How does a career gap affect my income long term?',
  'What should I do first this month?',
];

const chatMessages = ref([
  { id: 1, role: 'advisor', text: 'Hi, I\'m your Horizon advisor. We\'ll keep this calm, practical, and fully in your control.' },
]);

const selectedPath = ref(null);

const basePaths = [
  { id: 'career', emoji: '🚀', name: 'Career First', fertilityBase: 86, incomeBase: 315000, tradeoff: 'Maximizes income upside, with less flexibility later.', firstStep: 'Book a fertility consultation — it\'s just information, not a commitment.' },
  { id: 'balanced', emoji: '⚖️', name: 'Balanced', fertilityBase: 90, incomeBase: 265000, tradeoff: 'Steady growth with optionality preserved on both fronts.', firstStep: 'Create a 12-month plan with one milestone for career and one for family.' },
  { id: 'family', emoji: '🌱', name: 'Family Early', fertilityBase: 94, incomeBase: 225000, tradeoff: 'Highest near-term family probability, slower early income ramp.', firstStep: 'Map a support network and a re-entry strategy to protect momentum.' },
];

const industryBoost = {
  Tech: 1.12,
  Finance: 1.15,
  Healthcare: 1.08,
  Creative: 0.95,
  Other: 1.0,
};

const intentBoost = {
  'Definitely want kids': 4,
  'Open to it': 1,
  Unsure: -2,
};

const paths = computed(() => {
  return basePaths.map((p) => {
    const agePenalty = Math.max(0, profile.value.age - 30) * 1.2;
    const freezeBoost = simulation.value.eggFreezeAge <= 30 ? 3 : 1;
    const fertility = Math.max(58, Math.round(p.fertilityBase - agePenalty + freezeBoost + intentBoost[profile.value.familyIntention]));

    const goalMultiplier = profile.value.goal === 'Make Partner/Executive' ? 1.18 : profile.value.goal === 'Build My Own Thing' ? 1.12 : 0.96;
    const delayPenalty = simulation.value.delayYears * 0.045;
    const income = Math.round(p.incomeBase * industryBoost[profile.value.industry] * goalMultiplier * (1 - delayPenalty));

    return { ...p, fertility, income };
  });
});

const fertilityPoints = computed(() => chartPoints((age) => Math.max(40, 98 - (age - 25) * 2.5 + (simulation.value.eggFreezeAge <= 30 ? 5 : 1))));
const incomePoints = computed(() => chartPoints((age) => {
  const slope = 3.8 - simulation.value.delayYears * 0.4;
  return Math.min(100, 18 + (age - 25) * slope);
}));

const confettiDots = computed(() =>
  Array.from({ length: 28 }, (_, i) => ({
    id: i,
    style: {
      left: `${Math.random() * 100}%`,
      top: `${Math.random() * 100}%`,
      animationDelay: `${Math.random() * 1.8}s`,
      background: i % 2 ? '#A78BFA' : '#C9956C',
    },
  })),
);

function chartPoints(valueFn) {
  const points = [];
  for (let age = 25; age <= 45; age += 1) {
    const x = 40 + ((age - 25) / 20) * 640;
    const y = 220 - (valueFn(age) / 100) * 200;
    points.push(`${x},${y}`);
  }
  return points.join(' ');
}

function nextQuizStep() {
  if (quizStep.value < 5) {
    quizStep.value += 1;
    return;
  }
  stage.value = 'dashboard';
}

function selectPath(path) {
  selectedPath.value = path;
  stage.value = 'action';
}

function sendPrompt(prompt) {
  chatMessages.value.push({ id: Date.now(), role: 'user', text: prompt });

  const responseMap = {
    "What's the difference between freezing eggs at 28 vs 32?": 'Freezing earlier often means a higher expected egg quality and fewer cycles. Many clinics report better yield in the late 20s versus early 30s. [ASRM, CDC]',
    'How does a career gap affect my income long term?': 'A short planned gap can reduce 10-year income by 6–15%, but re-entry strategy, upskilling, and sponsor support can narrow that. [McKinsey Women in Workplace]',
    'What should I do first this month?': 'Start with one consult and one money move: schedule an informational fertility consult and set up an automated investment transfer.',
  };

  setTimeout(() => {
    chatMessages.value.push({ id: Date.now() + 1, role: 'advisor', text: responseMap[prompt] });
  }, 450);
}
</script>

<style scoped>
.horizon-app {
  background:
    radial-gradient(circle at 10% 10%, rgba(167, 139, 250, 0.2), transparent 40%),
    radial-gradient(circle at 90% 0%, rgba(201, 149, 108, 0.24), transparent 35%),
    linear-gradient(145deg, #0d0f1a 0%, #17172b 46%, #231931 100%);
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.35s ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.25s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(14px);
}

.confetti {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 999px;
  opacity: 0.7;
  animation: confetti 2.2s ease-in-out infinite;
}

@keyframes confetti {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-22px);
  }
}
</style>
