import json

with open("debug_logs/questions_8_2.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Build HTML template
html_template = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>國中文言成語挑戰殿堂 · 8上第2次段考專區</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Vue 3 CDN -->
  <script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>
  <!-- Canvas Confetti CDN -->
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
  <!-- Google Fonts: Noto Serif TC & Noto Sans TC -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@600;900&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            serif: ['"Noto Serif TC"', 'serif'],
            sans: ['"Noto Sans TC"', 'sans-serif'],
          },
          colors: {
            heritage: {
              50: '#f4f7f5',
              100: '#e5ece7',
              200: '#ccdad1',
              500: '#3d6b52',
              600: '#2d523e',
              700: '#213f2f',
              800: '#182f23',
              900: '#102018',
            },
            amberGold: {
              400: '#fbbf24',
              500: '#d97706',
              600: '#b45309',
            }
          }
        }
      }
    }
  </script>
  <style>
    [v-cloak] { display: none; }
    .glass-card {
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      box-shadow: 0 8px 32px rgba(16, 32, 24, 0.08);
    }
    .shake {
      animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
    }
    @keyframes shake {
      10%, 90% { transform: translate3d(-2px, 0, 0); }
      20%, 80% { transform: translate3d(4px, 0, 0); }
      30%, 50%, 70% { transform: translate3d(-6px, 0, 0); }
      40%, 60% { transform: translate3d(6px, 0, 0); }
    }
    .pop-in {
      animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }
    @keyframes popIn {
      0% { opacity: 0; transform: scale(0.85); }
      100% { opacity: 1; transform: scale(1); }
    }
  </style>
</head>
<body class="bg-gradient-to-br from-[#f2f6f3] via-[#e8efe9] to-[#dbe7dc] min-h-screen text-stone-800 font-sans selection:bg-heritage-500 selection:text-white">

<div id="app" v-cloak class="max-w-4xl mx-auto px-4 py-6 md:py-8 min-h-screen flex flex-col justify-between">

  <!-- ==================== HEADER ==================== -->
  <header class="mb-6 flex flex-col sm:flex-row items-center justify-between gap-4 border-b border-heritage-200 pb-4">
    <div class="flex items-center gap-3 cursor-pointer" @click="goHome">
      <div class="w-12 h-12 rounded-xl bg-heritage-700 text-amberGold-400 flex items-center justify-center font-serif text-2xl font-black shadow-md border border-amberGold-500/40">
        典
      </div>
      <div>
        <h1 class="text-xl sm:text-2xl font-black font-serif tracking-wide text-heritage-900">國中文言成語挑戰殿堂</h1>
        <p class="text-xs sm:text-sm text-heritage-600 font-medium">教育部成語典檢測 · 八年級上學期第 2 次段考專區</p>
      </div>
    </div>
    <div class="flex items-center gap-2">
      <!-- Sound toggle -->
      <button @click="toggleSound" :title="soundEnabled ? '靜音' : '開啟音效'" class="px-3 py-1.5 rounded-lg border border-heritage-300 bg-white/80 hover:bg-white text-stone-700 text-sm font-medium transition flex items-center gap-1.5 shadow-sm">
        <span>{{ soundEnabled ? '🔊 音效開' : '🔇 靜音' }}</span>
      </button>
      <!-- Badges shortcut -->
      <button @click="view = 'badges'" :class="{'bg-amberGold-500 text-white': view === 'badges', 'bg-white/80 text-stone-700': view !== 'badges'}" class="px-3 py-1.5 rounded-lg border border-heritage-300 hover:bg-amberGold-50 text-sm font-bold transition flex items-center gap-1.5 shadow-sm">
        <span>🏅 勳章館</span>
        <span class="bg-amber-100 text-amber-800 text-xs px-1.5 py-0.5 rounded-full font-black">{{ unlockedBadgesCount }}/9</span>
      </button>
      <!-- Wrong questions shortcut -->
      <button @click="view = 'wrong_notebook'" :class="{'bg-rose-600 text-white': view === 'wrong_notebook', 'bg-white/80 text-stone-700': view !== 'wrong_notebook'}" class="px-3 py-1.5 rounded-lg border border-heritage-300 hover:bg-rose-50 text-sm font-bold transition flex items-center gap-1.5 shadow-sm">
        <span>📖 錯題本</span>
        <span v-if="wrongNotebook.length > 0" class="bg-rose-100 text-rose-700 text-xs px-1.5 py-0.5 rounded-full font-black">{{ wrongNotebook.length }}</span>
      </button>
    </div>
  </header>

  <!-- ==================== VIEW 1: HOME (單元與模式選擇) ==================== -->
  <main v-if="view === 'home'" class="flex-1 space-y-6">
    <!-- Big Banner -->
    <div class="glass-card rounded-2xl p-6 sm:p-8 border border-heritage-200/80 relative overflow-hidden">
      <div class="absolute -right-8 -bottom-8 w-48 h-48 bg-heritage-500/10 rounded-full blur-2xl pointer-events-none"></div>
      <div class="relative z-10">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-heritage-100 text-heritage-800 text-xs font-bold mb-3 border border-heritage-200">
          <span>🎯 本次測驗範圍：第 29 ～ 32 列</span>
          <span>•</span>
          <span>共 100 則核心成語</span>
        </div>
        <h2 class="text-2xl sm:text-3xl font-black font-serif text-heritage-900 mb-2">精熟練習 × 段考模擬抽測</h2>
        <p class="text-stone-600 text-sm sm:text-base leading-relaxed max-w-2xl">
          依據國中課綱與段考進度，挑選 8 上第 2 次段考範圍成語。提供「逐列精熟學習」與「隨機抽 20 題模擬考」雙軌挑戰，考後解鎖評定等級與成就獎章！
        </p>

        <!-- Stats Bar -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-5 border-t border-heritage-200/60">
          <div class="bg-white/60 p-3 rounded-xl border border-heritage-100">
            <div class="text-xs text-stone-500 font-medium">段考抽測最高分</div>
            <div class="text-xl font-black text-heritage-700">{{ stats.examBestScore !== null ? stats.examBestScore + ' 分' : '尚未測驗' }}</div>
          </div>
          <div class="bg-white/60 p-3 rounded-xl border border-heritage-100">
            <div class="text-xs text-stone-500 font-medium">段考評定稱號</div>
            <div class="text-xl font-black text-amberGold-600">{{ getRankTitle(stats.examBestScore) }}</div>
          </div>
          <div class="bg-white/60 p-3 rounded-xl border border-heritage-100">
            <div class="text-xs text-stone-500 font-medium">小單元通關進度</div>
            <div class="text-xl font-black text-heritage-700">{{ masteredUnitsCount }} / 4 單元</div>
          </div>
          <div class="bg-white/60 p-3 rounded-xl border border-heritage-100">
            <div class="text-xs text-stone-500 font-medium">累計榮譽獎章</div>
            <div class="text-xl font-black text-amberGold-600">{{ unlockedBadgesCount }} / 9 枚</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Exam Simulation Mode Hero Box -->
    <div class="glass-card rounded-2xl p-6 border-2 border-amberGold-400/80 bg-gradient-to-r from-amber-50/80 to-white hover:shadow-lg transition">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div class="inline-flex items-center gap-1.5 text-xs font-black text-amber-700 bg-amber-200/80 px-2.5 py-0.5 rounded-md mb-2">
            <span>🔥 模式二 · 模擬段考衝刺</span>
            <span>•</span>
            <span>隨機 20 題</span>
          </div>
          <h3 class="text-xl font-black font-serif text-heritage-900">8 上第 2 次段考 · 綜合能力隨機抽測</h3>
          <p class="text-xs sm:text-sm text-stone-600 mt-1">從本大單元 4 列（100 則成語）中隨機挑選 20 題，全卷答完統一結算，模擬真實段考考驗！</p>
        </div>
        <button @click="startExamMode" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-gradient-to-r from-amberGold-500 to-amberGold-600 hover:from-amberGold-600 hover:to-amber-700 text-white font-bold text-base shadow-md hover:shadow-lg transition flex items-center justify-center gap-2 whitespace-nowrap">
          <span>🚀 開始段考抽測</span>
          <span class="text-xs opacity-90">(20題)</span>
        </button>
      </div>
    </div>

    <!-- Mode 1: 4 Mini Units Grid -->
    <div>
      <div class="flex items-center justify-between mb-3">
        <h3 class="text-lg font-bold font-serif text-heritage-900 flex items-center gap-2">
          <span>📚 模式一 · 逐列小單元精熟練習</span>
          <span class="text-xs font-sans font-normal text-stone-500">(每列 25 題 · 答對即刻反饋)</span>
        </h3>
        <button @click="view = 'cards'" class="text-xs text-heritage-600 hover:text-heritage-800 font-bold underline">
          📖 瀏覽全部 100 則成語卡
        </button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div v-for="u in unitList" :key="u.id" class="glass-card rounded-xl p-5 border border-heritage-200 hover:border-heritage-500 transition group flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-black px-2.5 py-0.5 rounded-full bg-heritage-100 text-heritage-800 border border-heritage-200">
                小單元 {{ u.id }} · {{ u.rowName }}
              </span>
              <span v-if="stats.unitPassed[u.id]" class="text-xs font-bold text-amber-600 flex items-center gap-1">
                ⭐ 最高分: {{ stats.unitBestScore[u.id] }}分
              </span>
              <span v-else class="text-xs text-stone-400 font-medium">未完成</span>
            </div>
            <h4 class="text-base font-bold text-heritage-900 mb-1 group-hover:text-heritage-700 transition">
              {{ u.title }}
            </h4>
            <p class="text-xs text-stone-500 leading-relaxed mb-4">
              {{ u.sampleIdioms }}
            </p>
          </div>
          <div class="flex items-center justify-between pt-3 border-t border-heritage-100">
            <span class="text-xs text-stone-500 font-medium">全卷共 25 題</span>
            <button @click="startUnitMode(u.id)" class="px-4 py-1.5 rounded-lg bg-heritage-700 hover:bg-heritage-800 text-white text-xs font-bold transition shadow-sm">
              {{ stats.unitPassed[u.id] ? '再練一次' : '開始練習' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Future Scope Teaser Bar -->
    <div class="p-4 rounded-xl bg-heritage-100/50 border border-heritage-200 text-xs text-stone-600 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
      <div>
        <span class="font-bold text-heritage-900">📌 全書段考藍圖：</span>
        <span>7上(3段) ~ 9下(2段) 共 17 個大單元 (68列) + 「其實還有」擴充挑戰區 (12列)。目前已啟用 8上2段 (第29~32列)。</span>
      </div>
      <button @click="showRoadmapModal = true" class="text-heritage-700 hover:underline font-bold whitespace-nowrap">
        查看完整 17 次段考排程 ➔
      </button>
    </div>
  </main>

  <!-- ==================== VIEW 2: QUIZ INTERFACE ==================== -->
  <main v-if="view === 'quiz'" class="flex-1 space-y-6">
    <!-- Quiz Header Bar -->
    <div class="glass-card rounded-xl p-4 border border-heritage-200 flex items-center justify-between gap-3 shadow-sm">
      <div class="flex items-center gap-2">
        <button @click="confirmQuitQuiz" class="px-2.5 py-1 rounded-lg border border-stone-300 hover:bg-stone-100 text-xs font-bold text-stone-600 transition">
          ✕ 退出
        </button>
        <div>
          <span class="text-xs font-black text-heritage-700 bg-heritage-100 px-2 py-0.5 rounded">
            {{ quizConfig.mode === 'unit' ? '模式一：小單元練習' : (quizConfig.mode === 'wrong' ? '錯題消滅戰' : '模式二：段考模擬考') }}
          </span>
          <span class="ml-2 text-xs text-stone-500 font-medium">{{ quizConfig.title }}</span>
        </div>
      </div>
      <div class="flex items-center gap-4">
        <!-- Timer for Exam Mode -->
        <div v-if="quizConfig.mode === 'exam'" class="text-xs font-mono font-bold text-stone-600 bg-stone-100 px-2.5 py-1 rounded-md">
          ⏱️ {{ formatTime(elapsedSeconds) }}
        </div>
        <!-- Progress Counter -->
        <div class="text-sm font-black text-heritage-800">
          <span class="text-lg text-heritage-600">{{ currentQuestionIndex + 1 }}</span>
          <span class="text-stone-400"> / {{ currentQuestions.length }}</span>
        </div>
      </div>
    </div>

    <!-- Progress Bar -->
    <div class="w-full bg-heritage-200/60 rounded-full h-2 overflow-hidden">
      <div class="bg-heritage-600 h-2 rounded-full transition-all duration-300" :style="{ width: ((currentQuestionIndex + 1) / currentQuestions.length * 100) + '%' }"></div>
    </div>

    <!-- Question Card -->
    <div class="glass-card rounded-2xl p-6 sm:p-8 border border-heritage-200 shadow-md relative" :class="{'shake': isShaking}">
      <div class="flex items-center justify-between text-xs text-stone-500 mb-4 pb-2 border-b border-heritage-100">
        <span>題號 {{ currentQuestionIndex + 1 }}</span>
        <button v-if="quizConfig.mode === 'unit'" @click="showHint = !showHint" class="text-heritage-600 hover:text-heritage-800 font-bold underline flex items-center gap-1">
          💡 {{ showHint ? '隱藏成語提示' : '成語提示' }}
        </button>
      </div>

      <!-- Hint Box in Unit Mode -->
      <div v-if="showHint && quizConfig.mode === 'unit'" class="mb-4 p-3 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-900 pop-in">
        <span class="font-bold">【釋義提示】</span> {{ currentQ.meaning }}
      </div>

      <!-- Sentence Text -->
      <div class="text-lg sm:text-2xl font-serif leading-relaxed text-stone-900 mb-8 select-none">
        <template v-for="(seg, idx) in formatSentence(currentQ.sentence)" :key="idx">
          <span v-if="seg.isBlank" class="inline-block px-3 py-1 mx-1 rounded-lg bg-heritage-100 border-2 border-dashed border-heritage-500 text-heritage-800 font-bold text-xl min-w-[7rem] text-center shadow-inner">
            {{ userSelectedOption ? userSelectedOption : '【　　】' }}
          </span>
          <span v-else>{{ seg.text }}</span>
        </template>
      </div>

      <!-- 4 Options Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <button 
          v-for="(opt, oIdx) in currentQ.options" 
          :key="oIdx"
          @click="selectOption(opt)"
          :disabled="quizConfig.mode === 'unit' && answeredCurrent"
          :class="getOptionClass(opt)"
          class="p-4 rounded-xl border text-left font-serif text-base sm:text-lg font-bold transition flex items-center justify-between group shadow-sm">
          <div class="flex items-center gap-3">
            <span class="w-7 h-7 rounded-lg bg-stone-100 group-hover:bg-heritage-100 text-stone-700 text-xs font-mono font-bold flex items-center justify-center border border-stone-200">
              {{ ['A', 'B', 'C', 'D'][oIdx] }}
            </span>
            <span>{{ opt }}</span>
          </div>
          <!-- Indicator Icon -->
          <div v-if="answeredCurrent">
            <span v-if="opt === currentQ.answer" class="text-emerald-600 font-black text-xl">✓</span>
            <span v-else-if="userSelectedOption === opt" class="text-rose-600 font-black text-xl">✕</span>
          </div>
        </button>
      </div>

      <!-- Unit Mode Instant Explanation Box -->
      <div v-if="quizConfig.mode === 'unit' && answeredCurrent" class="mt-6 pt-5 border-t border-heritage-100 pop-in">
        <div :class="userSelectedOption === currentQ.answer ? 'bg-emerald-50 border-emerald-200 text-emerald-950' : 'bg-rose-50 border-rose-200 text-rose-950'" class="p-4 rounded-xl border mb-4">
          <div class="flex items-center gap-2 font-bold mb-1">
            <span v-if="userSelectedOption === currentQ.answer" class="text-emerald-700 text-lg">🎉 答對了！</span>
            <span v-else class="text-rose-700 text-lg">⚠️ 答錯囉！正解是：<strong class="underline font-serif text-rose-900">{{ currentQ.answer }}</strong></span>
          </div>
          <p class="text-xs sm:text-sm leading-relaxed mb-2">{{ currentQ.explanation }}</p>
          <div class="text-xs text-stone-600 font-medium">
            <span class="font-bold">【成語釋義】</span> {{ currentQ.meaning }} (注音: {{ currentQ.pinyin }})
          </div>
        </div>

        <button @click="nextQuestion" class="w-full py-3 rounded-xl bg-heritage-700 hover:bg-heritage-800 text-white font-bold text-sm shadow-md transition flex items-center justify-center gap-2">
          <span>{{ currentQuestionIndex + 1 < currentQuestions.length ? '下一題 ➔' : '結算成績 🏆' }}</span>
        </button>
      </div>

      <!-- Exam Mode Navigation Buttons -->
      <div v-if="quizConfig.mode === 'exam'" class="mt-6 pt-5 border-t border-heritage-100 flex items-center justify-between gap-3">
        <button @click="prevQuestion" :disabled="currentQuestionIndex === 0" class="px-4 py-2 rounded-lg border border-stone-300 hover:bg-stone-100 disabled:opacity-40 disabled:hover:bg-transparent text-xs font-bold transition">
          ⬅ 上一題
        </button>
        <div class="flex items-center gap-2">
          <button @click="showExamDrawer = !showExamDrawer" class="px-3 py-2 rounded-lg border border-heritage-300 bg-heritage-50 text-heritage-800 text-xs font-bold hover:bg-heritage-100 transition">
            📋 答題卡 ({{ answeredCount }}/{{ currentQuestions.length }})
          </button>
          <button v-if="currentQuestionIndex + 1 < currentQuestions.length" @click="nextQuestion" class="px-5 py-2 rounded-lg bg-heritage-700 hover:bg-heritage-800 text-white text-xs font-bold transition shadow-sm">
            下一題 ➔
          </button>
          <button v-else @click="confirmSubmitExam" class="px-5 py-2 rounded-lg bg-amberGold-500 hover:bg-amberGold-600 text-white text-xs font-bold transition shadow-sm">
            交卷結算 🏆
          </button>
        </div>
      </div>
    </div>

    <!-- Exam Mode Jump Drawer Modal -->
    <div v-if="showExamDrawer && quizConfig.mode === 'exam'" class="glass-card rounded-2xl p-5 border border-heritage-300 pop-in">
      <div class="flex items-center justify-between mb-3">
        <h4 class="text-sm font-bold text-heritage-900">快速題目跳轉卡</h4>
        <button @click="showExamDrawer = false" class="text-xs text-stone-500 hover:text-stone-800">關閉 ✕</button>
      </div>
      <div class="grid grid-cols-5 sm:grid-cols-10 gap-2 mb-4">
        <button 
          v-for="(q, idx) in currentQuestions" 
          :key="idx" 
          @click="currentQuestionIndex = idx; showExamDrawer = false"
          :class="{
            'bg-heritage-600 text-white font-bold ring-2 ring-heritage-400': currentQuestionIndex === idx,
            'bg-emerald-100 text-emerald-800 border border-emerald-300': examAnswers[idx] && currentQuestionIndex !== idx,
            'bg-stone-100 text-stone-600 border border-stone-200': !examAnswers[idx] && currentQuestionIndex !== idx
          }"
          class="h-9 rounded-lg text-xs font-bold transition flex items-center justify-center">
          {{ idx + 1 }}
        </button>
      </div>
      <div class="flex items-center justify-between">
        <div class="text-xs text-stone-500">
          已作答: <span class="font-bold text-emerald-700">{{ answeredCount }}</span> 題 / 未作答: <span class="font-bold text-rose-600">{{ currentQuestions.length - answeredCount }}</span> 題
        </div>
        <button @click="confirmSubmitExam" class="px-4 py-1.5 rounded-lg bg-amberGold-500 text-white text-xs font-bold hover:bg-amberGold-600 transition">
          直接交卷
        </button>
      </div>
    </div>
  </main>

  <!-- ==================== VIEW 3: RESULT SCREEN ==================== -->
  <main v-if="view === 'result'" class="flex-1 space-y-6 pop-in">
    <!-- Big Result Card -->
    <div class="glass-card rounded-3xl p-6 sm:p-10 border border-heritage-200 text-center relative overflow-hidden shadow-lg">
      <div class="inline-block px-4 py-1 rounded-full text-xs font-bold mb-3" :class="lastResult.score >= 85 ? 'bg-amber-100 text-amber-900 border border-amber-300' : 'bg-heritage-100 text-heritage-800'">
        {{ lastResult.title }} · 測驗結果結算
      </div>

      <!-- Score Big Number -->
      <div class="flex items-baseline justify-center gap-1 my-3">
        <span class="text-6xl sm:text-7xl font-black font-serif tracking-tight" :class="lastResult.score >= 85 ? 'text-amberGold-600' : (lastResult.score >= 60 ? 'text-heritage-700' : 'text-stone-700')">
          {{ lastResult.score }}
        </span>
        <span class="text-stone-400 text-xl font-bold">/ 100 分</span>
      </div>

      <!-- Rank Title -->
      <div class="text-2xl sm:text-3xl font-black font-serif text-heritage-900 mb-2">
        {{ getRankTitle(lastResult.score) }}
      </div>

      <!-- Encouragement Message -->
      <p class="text-stone-600 text-sm sm:text-base max-w-lg mx-auto leading-relaxed mb-6">
        {{ getEncouragement(lastResult.score) }}
      </p>

      <!-- New Unlocked Badge Alert if any -->
      <div v-if="lastResult.newBadges.length > 0" class="mb-6 p-4 rounded-2xl bg-amber-50 border-2 border-amberGold-400/80 text-left pop-in">
        <div class="text-xs font-black text-amber-800 uppercase tracking-wider mb-2 flex items-center gap-1.5">
          <span>🎉 恭喜解鎖全新榮譽勳章！</span>
        </div>
        <div class="flex flex-wrap gap-3">
          <div v-for="b in lastResult.newBadges" :key="b.id" class="flex items-center gap-2 bg-white px-3 py-2 rounded-xl border border-amber-200 shadow-sm">
            <span class="text-2xl">{{ b.icon }}</span>
            <div>
              <div class="text-xs font-bold text-stone-900">{{ b.name }}</div>
              <div class="text-[10px] text-stone-500">{{ b.desc }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Summary Grid -->
      <div class="grid grid-cols-3 gap-3 max-w-md mx-auto pt-6 border-t border-heritage-100">
        <div class="bg-emerald-50/60 p-2.5 rounded-xl border border-emerald-100">
          <div class="text-[11px] text-emerald-800 font-medium">答對題數</div>
          <div class="text-lg font-black text-emerald-700">{{ lastResult.correctCount }} 題</div>
        </div>
        <div class="bg-rose-50/60 p-2.5 rounded-xl border border-rose-100">
          <div class="text-[11px] text-rose-800 font-medium">答錯題數</div>
          <div class="text-lg font-black text-rose-700">{{ lastResult.wrongCount }} 題</div>
        </div>
        <div class="bg-stone-50 p-2.5 rounded-xl border border-stone-200">
          <div class="text-[11px] text-stone-600 font-medium">作答用時</div>
          <div class="text-lg font-black text-stone-700">{{ formatTime(lastResult.timeSpent) }}</div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-wrap items-center justify-center gap-3 mt-8">
        <button v-if="lastResult.wrongCount > 0" @click="startWrongQuestionsQuiz" class="px-6 py-3 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-bold text-sm shadow-md transition flex items-center gap-2">
          <span>🔥 立即消滅錯題 ({{ lastResult.wrongCount }}題)</span>
        </button>
        <button @click="restartCurrentQuiz" class="px-5 py-3 rounded-xl bg-heritage-700 hover:bg-heritage-800 text-white font-bold text-sm shadow-md transition">
          🔄 再測一次
        </button>
        <button @click="view = 'badges'" class="px-5 py-3 rounded-xl bg-amberGold-500 hover:bg-amberGold-600 text-white font-bold text-sm shadow-md transition">
          🏅 查看勳章館
        </button>
        <button @click="goHome" class="px-5 py-3 rounded-xl border border-heritage-300 hover:bg-white text-stone-700 font-bold text-sm transition">
          🏠 返回首頁
        </button>
      </div>
    </div>

    <!-- Review Section for Wrong Questions -->
    <div v-if="lastResult.wrongItems.length > 0" class="glass-card rounded-2xl p-6 border border-heritage-200">
      <h3 class="text-lg font-bold font-serif text-heritage-900 mb-4 flex items-center gap-2">
        <span>🔍 錯題詳細解析與辨析</span>
        <span class="text-xs font-sans text-rose-600 font-normal">（共 {{ lastResult.wrongItems.length }} 題，已自動收錄至錯題本）</span>
      </h3>
      <div class="space-y-4">
        <div v-for="(item, idx) in lastResult.wrongItems" :key="idx" class="p-4 rounded-xl border border-rose-200 bg-rose-50/40">
          <div class="flex items-start justify-between gap-2 mb-2">
            <span class="text-xs font-black px-2 py-0.5 rounded bg-rose-200 text-rose-900">錯題 {{ idx + 1 }}</span>
            <span class="text-xs text-stone-500">{{ item.q.unit_name }}</span>
          </div>
          <div class="text-base font-serif text-stone-900 mb-2 leading-relaxed">
            {{ item.q.sentence.replace('【　　】', '【 ' + item.q.answer + ' 】') }}
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs mb-3">
            <div class="p-2 rounded bg-white border border-rose-100">
              <span class="text-rose-600 font-bold">你的答案：</span> {{ item.chosen || '未作答' }}
            </div>
            <div class="p-2 rounded bg-white border border-emerald-200">
              <span class="text-emerald-700 font-bold">正確成語：</span> <strong class="font-serif text-emerald-800 text-sm">{{ item.q.answer }}</strong> ({{ item.q.pinyin }})
            </div>
          </div>
          <div class="text-xs text-stone-700 leading-relaxed bg-white/80 p-3 rounded-lg border border-stone-200">
            <div class="font-bold text-heritage-800 mb-1">【解析說明】</div>
            <p>{{ item.q.explanation }}</p>
            <div class="mt-1 text-stone-500"><strong class="text-stone-700">成語釋義：</strong>{{ item.q.meaning }}</div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <!-- ==================== VIEW 4: BADGES SHOWCASE ==================== -->
  <main v-if="view === 'badges'" class="flex-1 space-y-6 pop-in">
    <div class="glass-card rounded-2xl p-6 border border-heritage-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div>
        <div class="text-xs font-bold text-heritage-600 uppercase tracking-wider mb-1">成就榮譽圖鑑</div>
        <h2 class="text-2xl font-black font-serif text-heritage-900">8 上第 2 次段考 · 專屬勳章博古架</h2>
        <p class="text-xs sm:text-sm text-stone-500 mt-1">完成小單元精熟與段考抽測，收集專屬國風榮譽勳章！</p>
      </div>
      <div class="text-right">
        <div class="text-xs text-stone-500 font-medium">解鎖達成率</div>
        <div class="text-2xl font-black text-amberGold-600">{{ unlockedBadgesCount }} / {{ badgeList.length }}</div>
      </div>
    </div>

    <!-- Badge Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div 
        v-for="b in badgeList" 
        :key="b.id"
        @click="selectedBadge = b"
        :class="stats.badges[b.id] ? 'bg-gradient-to-b from-amber-50 to-white border-amberGold-400 shadow-md ring-1 ring-amber-300' : 'bg-stone-50/80 border-stone-200 opacity-60'"
        class="glass-card rounded-2xl p-5 border text-center transition cursor-pointer hover:scale-[1.02] flex flex-col items-center justify-between">
        <div>
          <div class="text-4xl sm:text-5xl my-3 filter" :class="{'grayscale': !stats.badges[b.id]}">
            {{ b.icon }}
          </div>
          <h4 class="font-bold font-serif text-base text-stone-900 mb-1">{{ b.name }}</h4>
          <p class="text-xs text-stone-500 leading-relaxed mb-3">{{ b.desc }}</p>
        </div>
        <div class="w-full pt-3 border-t border-stone-200/60 text-xs">
          <span v-if="stats.badges[b.id]" class="text-emerald-700 font-bold flex items-center justify-center gap-1">
            ✓ 已解鎖 ({{ stats.badges[b.id].date }})
          </span>
          <span v-else class="text-stone-400 font-medium">
            🔒 尚未解鎖 (點擊看條件)
          </span>
        </div>
      </div>
    </div>

    <div class="text-center pt-4">
      <button @click="goHome" class="px-6 py-2.5 rounded-xl border border-heritage-300 hover:bg-white text-stone-700 font-bold text-sm transition">
        ➔ 返回單元首頁
      </button>
    </div>
  </main>

  <!-- ==================== VIEW 5: WRONG QUESTIONS NOTEBOOK ==================== -->
  <main v-if="view === 'wrong_notebook'" class="flex-1 space-y-6 pop-in">
    <div class="glass-card rounded-2xl p-6 border border-heritage-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div>
        <div class="text-xs font-bold text-rose-600 uppercase tracking-wider mb-1">個人複習錦囊</div>
        <h2 class="text-2xl font-black font-serif text-heritage-900">錯題強化專屬筆記本</h2>
        <p class="text-xs sm:text-sm text-stone-500 mt-1">針對歷次練習與測驗中答錯的題目進行集中複習與重測！</p>
      </div>
      <div v-if="wrongNotebook.length > 0" class="flex gap-2">
        <button @click="startWrongQuestionsQuiz" class="px-5 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-bold text-sm shadow-md transition flex items-center gap-1.5">
          <span>🔥 消滅錯題挑戰 ({{ wrongNotebook.length }}題)</span>
        </button>
        <button @click="clearWrongNotebook" class="px-3 py-2.5 rounded-xl border border-stone-300 hover:bg-stone-100 text-xs text-stone-600 transition">
          清空
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="wrongNotebook.length === 0" class="glass-card rounded-2xl p-12 text-center border border-heritage-200">
      <div class="text-5xl mb-3">🎉</div>
      <h3 class="text-xl font-bold font-serif text-heritage-900 mb-1">太厲害了！目前沒有任何錯題</h3>
      <p class="text-xs sm:text-sm text-stone-500 mb-6">您的成語掌握度極高，趕快進行段考抽測挑戰 100 分滿分金章吧！</p>
      <button @click="goHome" class="px-5 py-2.5 rounded-xl bg-heritage-700 text-white text-xs font-bold">
        返回首頁
      </button>
    </div>

    <!-- Wrong Questions List -->
    <div v-else class="space-y-4">
      <div v-for="(item, idx) in wrongNotebook" :key="idx" class="glass-card rounded-xl p-5 border border-rose-200">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-black text-rose-800 bg-rose-100 px-2 py-0.5 rounded">
            錯題 {{ idx + 1 }} · {{ item.q.unit_name }}
          </span>
          <button @click="removeSingleWrong(idx)" class="text-xs text-stone-400 hover:text-rose-600">
            移除此題 ✕
          </button>
        </div>
        <div class="text-base font-serif text-stone-900 mb-2 leading-relaxed">
          {{ item.q.sentence.replace('【　　】', '【 ' + item.q.answer + ' 】') }}
        </div>
        <div class="bg-white p-3 rounded-lg border border-stone-200 text-xs leading-relaxed">
          <div class="font-bold text-emerald-800 mb-1">正解：{{ item.q.answer }} ({{ item.q.pinyin }})</div>
          <div class="text-stone-700 mb-1"><strong>釋義：</strong>{{ item.q.meaning }}</div>
          <div class="text-stone-500"><strong>解析：</strong>{{ item.q.explanation }}</div>
        </div>
      </div>
    </div>
  </main>

  <!-- ==================== VIEW 6: CARDS (成語典題庫全覽) ==================== -->
  <main v-if="view === 'cards'" class="flex-1 space-y-6 pop-in">
    <div class="glass-card rounded-2xl p-6 border border-heritage-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div>
        <div class="text-xs font-bold text-heritage-600 uppercase tracking-wider mb-1">8上第2次段考 · 題庫全覽</div>
        <h2 class="text-2xl font-black font-serif text-heritage-900">100 則核心成語知識卡</h2>
        <p class="text-xs sm:text-sm text-stone-500 mt-1">隨時查閱成語注音、典故釋義、生活情境例句與考點解析。</p>
      </div>
      <!-- Search Input -->
      <div class="w-full sm:w-64">
        <input v-model="cardSearch" type="text" placeholder="🔍 搜尋成語或關鍵字..." class="w-full px-3.5 py-2 rounded-xl border border-heritage-300 text-sm focus:outline-none focus:ring-2 focus:ring-heritage-500 bg-white">
      </div>
    </div>

    <!-- Filter by Unit Tabs -->
    <div class="flex items-center gap-2 overflow-x-auto pb-2">
      <button @click="cardFilterUnit = 0" :class="cardFilterUnit === 0 ? 'bg-heritage-700 text-white font-bold' : 'bg-white text-stone-600 hover:bg-stone-50'" class="px-3 py-1.5 rounded-lg border border-heritage-200 text-xs whitespace-nowrap transition">
        全部 (100則)
      </button>
      <button v-for="u in unitList" :key="u.id" @click="cardFilterUnit = u.id" :class="cardFilterUnit === u.id ? 'bg-heritage-700 text-white font-bold' : 'bg-white text-stone-600 hover:bg-stone-50'" class="px-3 py-1.5 rounded-lg border border-heritage-200 text-xs whitespace-nowrap transition">
        小單元 {{ u.id }} (25則)
      </button>
    </div>

    <!-- Cards Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div v-for="q in filteredCards" :key="q.idiom" class="glass-card rounded-xl p-5 border border-heritage-200 hover:border-heritage-400 transition">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-bold text-heritage-600 bg-heritage-100 px-2 py-0.5 rounded">
            {{ q.unit_name }}
          </span>
          <span class="text-xs text-stone-400 font-mono">{{ q.pinyin }}</span>
        </div>
        <h3 class="text-xl font-black font-serif text-heritage-900 mb-1">{{ q.idiom }}</h3>
        <p class="text-xs font-medium text-stone-600 mb-3">{{ q.meaning }}</p>
        <div class="p-3 rounded-lg bg-stone-50 border border-stone-200 text-xs mb-2">
          <span class="font-bold text-heritage-800">【生活例句】</span>
          <div class="mt-1 text-stone-800 leading-relaxed font-serif">
            {{ q.sentence.replace('【　　】', '【 ' + q.idiom + ' 】') }}
          </div>
        </div>
        <div class="text-[11px] text-stone-500 leading-relaxed">
          <strong class="text-stone-700">解析：</strong>{{ q.explanation }}
        </div>
      </div>
    </div>
  </main>

  <!-- ==================== FOOTER ==================== -->
  <footer class="mt-8 pt-4 border-t border-heritage-200 text-center text-xs text-stone-500 flex flex-col sm:flex-row items-center justify-between gap-2">
    <div>
      國中文言成語檢測系統 · 教學專用單檔網頁程式 · 支援離線與本地儲存
    </div>
    <div class="flex items-center gap-3">
      <button @click="exportSaveData" class="hover:underline">匯出進度</button>
      <span>•</span>
      <button @click="resetAllProgress" class="text-rose-600 hover:underline">重置所有紀錄</button>
    </div>
  </footer>

  <!-- ==================== MODAL: BADGE DETAIL ==================== -->
  <div v-if="selectedBadge" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4 z-50 pop-in" @click.self="selectedBadge = null">
    <div class="bg-white rounded-2xl max-w-sm w-full p-6 text-center border border-heritage-300 shadow-2xl">
      <div class="text-6xl mb-3">{{ selectedBadge.icon }}</div>
      <h3 class="text-xl font-black font-serif text-stone-900 mb-1">{{ selectedBadge.name }}</h3>
      <div class="text-xs font-bold text-amberGold-600 mb-4">{{ stats.badges[selectedBadge.id] ? '已獲得此榮譽' : '尚未解鎖' }}</div>
      <p class="text-xs text-stone-600 leading-relaxed mb-4 p-3 bg-stone-50 rounded-xl border border-stone-200">
        <strong class="text-stone-900">【解鎖條件】</strong><br>{{ selectedBadge.condition }}
      </p>
      <div v-if="stats.badges[selectedBadge.id]" class="text-xs text-emerald-700 font-bold mb-4">
        獲得日期：{{ stats.badges[selectedBadge.id].date }}
      </div>
      <button @click="selectedBadge = null" class="w-full py-2.5 rounded-xl bg-heritage-700 text-white text-xs font-bold">
        確認
      </button>
    </div>
  </div>

  <!-- ==================== MODAL: ROADMAP ==================== -->
  <div v-if="showRoadmapModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4 z-50 pop-in" @click.self="showRoadmapModal = false">
    <div class="bg-white rounded-2xl max-w-xl w-full p-6 border border-heritage-300 shadow-2xl max-h-[85vh] flex flex-col">
      <div class="flex items-center justify-between pb-3 border-b border-stone-200 mb-4">
        <h3 class="text-lg font-black font-serif text-heritage-900">成語典 80 列 · 國中 17 次段考藍圖</h3>
        <button @click="showRoadmapModal = false" class="text-stone-400 hover:text-stone-700">✕</button>
      </div>
      <div class="overflow-y-auto space-y-3 pr-2 text-xs text-stone-700 leading-relaxed flex-1">
        <p class="text-stone-600">全書 8 頁跨頁，實體頁碼第 4～19 頁，每頁 5 列，共計 80 列。每 4 列一個大單元：</p>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
          <div class="p-2.5 rounded-lg border bg-stone-50">
            <strong>七年級上學期</strong><br>
            • 7上1段：第 1～4 列<br>
            • 7上2段：第 5～8 列<br>
            • 7上3段：第 9～12 列
          </div>
          <div class="p-2.5 rounded-lg border bg-stone-50">
            <strong>七年級下學期</strong><br>
            • 7下1段：第 13～16 列<br>
            • 7下2段：第 17～20 列<br>
            • 7下3段：第 21～24 列
          </div>
          <div class="p-2.5 rounded-lg border bg-amber-50 border-amber-300">
            <strong class="text-amber-900">八年級上學期 (當前啟用)</strong><br>
            • 8上1段：第 25～28 列<br>
            • <strong class="text-amber-800">8上2段：第 29～32 列 (已就緒 100題)</strong><br>
            • 8上3段：第 33～36 列
          </div>
          <div class="p-2.5 rounded-lg border bg-stone-50">
            <strong>八年級下學期</strong><br>
            • 8下1段：第 37～40 列<br>
            • 8下2段：第 41～44 列<br>
            • 8下3段：第 45～48 列
          </div>
          <div class="p-2.5 rounded-lg border bg-stone-50">
            <strong>九年級 (會考總衝刺)</strong><br>
            • 9上1段：第 49～52 列<br>
            • 9上2段：第 53～56 列<br>
            • 9上3段：第 57～60 列<br>
            • 9下1段：第 61～64 列<br>
            • 9下2段：第 65～68 列
          </div>
          <div class="p-2.5 rounded-lg border bg-heritage-50 border-heritage-300">
            <strong class="text-heritage-900">其實還有 (擴充挑戰區)</strong><br>
            • 第 69～80 列 (剩餘 12 列)<br>
            • 相當於 3 個完整大單元容量的高手包！
          </div>
        </div>
      </div>
      <div class="pt-4 border-t border-stone-200 mt-4 text-right">
        <button @click="showRoadmapModal = false" class="px-4 py-2 rounded-xl bg-heritage-700 text-white text-xs font-bold">
          關閉
        </button>
      </div>
    </div>
  </div>

</div>

<!-- Vue 3 App Logic -->
<script>
  const ALL_QUESTIONS = """ + json.dumps(questions, ensure_ascii=False) + """;

  const { createApp, ref, computed, onMounted, onUnmounted } = Vue;

  createApp({
    setup() {
      // Navigation views: 'home' | 'quiz' | 'result' | 'badges' | 'wrong_notebook' | 'cards'
      const view = ref('home');
      const soundEnabled = ref(true);
      const showHint = ref(false);
      const isShaking = ref(false);
      const showExamDrawer = ref(false);
      const showRoadmapModal = ref(false);
      const selectedBadge = ref(null);

      // Unit definition list
      const unitList = [
        { id: 1, rowName: "第 29 列 (8畫上)", title: "小單元 1：孤注一擲 ～ 拈花惹草", sampleIdioms: "孤注一擲、孤芳自賞、居安思危、忠言逆耳、披荊斬棘、拋磚引玉..." },
        { id: 2, rowName: "第 30 列 (8畫中)", title: "小單元 2：拍案叫絕 ～ 泥牛入海", sampleIdioms: "拍案叫絕、抱薪救火、明哲保身、東山再起、杯弓蛇影、欣欣向榮..." },
        { id: 3, rowName: "第 31 列 (8畫下)", title: "小單元 3：河東獅吼 ～ 臥薪嚐膽", sampleIdioms: "河東獅吼、沽名釣譽、物是人非、狐假虎威、空中樓閣、臥薪嚐膽..." },
        { id: 4, rowName: "第 32 列 (8畫末)", title: "小單元 4：花甲之年 ～ 門庭若市", sampleIdioms: "花言巧語、虎視眈眈、迎刃而解、近水樓臺、金科玉律、長驅直入..." }
      ];

      // Badges definition
      const badgeList = [
        { id: 'unit_1', name: '小單元 1 精熟星章', icon: '🌟', desc: '完成第 29 列練習並達到 80 分以上', condition: '小單元 1 測驗成績達 80 分' },
        { id: 'unit_2', name: '小單元 2 精熟星章', icon: '🌟', desc: '完成第 30 列練習並達到 80 分以上', condition: '小單元 2 測驗成績達 80 分' },
        { id: 'unit_3', name: '小單元 3 精熟星章', icon: '🌟', desc: '完成第 31 列練習並達到 80 分以上', condition: '小單元 3 測驗成績達 80 分' },
        { id: 'unit_4', name: '小單元 4 精熟星章', icon: '🌟', desc: '完成第 32 列練習並達到 80 分以上', condition: '小單元 4 測驗成績達 80 分' },
        { id: 'exam_bronze', name: '8上2段·通關銅章', icon: '🥉', desc: '8上第2次段考模擬抽測達 60 分及格', condition: '段考抽測模式獲得 60 分以上' },
        { id: 'exam_silver', name: '8上2段·拔萃銀章', icon: '🥈', desc: '8上第2次段考模擬抽測達 85 分以上', condition: '段考抽測模式獲得 85 分以上' },
        { id: 'exam_gold', name: '8上2段·滿貫金章', icon: '🥇', desc: '8上第2次段考模擬抽測 100 分滿分通關', condition: '段考抽測模式獲得 100 分滿分' },
        { id: 'wrong_cleaner', name: '錯題清道夫', icon: '🎯', desc: '在專屬錯題消滅戰中全數答對訂正完成', condition: '完成錯題消滅戰且得分 100 分' },
        { id: 'speed_master', name: '快思敏捷', icon: '⚡', desc: '在 2 分鐘內完成段考抽測 20 題且及格', condition: '段考抽測 120 秒內完成且及格' }
      ];

      // Local storage persistence
      const STORAGE_KEY = 'idiom_quiz_grade8_sem1_exam2_save_v1';
      const stats = ref({
        unitPassed: { 1: false, 2: false, 3: false, 4: false },
        unitBestScore: { 1: 0, 2: 0, 3: 0, 4: 0 },
        examBestScore: null,
        badges: {}
      });

      const wrongNotebook = ref([]);

      // Load saved state
      function loadState() {
        try {
          const raw = localStorage.getItem(STORAGE_KEY);
          if (raw) {
            const data = JSON.parse(raw);
            if (data.stats) stats.value = data.stats;
            if (data.wrongNotebook) wrongNotebook.value = data.wrongNotebook;
          }
        } catch(e) {
          console.error('Failed to load save:', e);
        }
      }

      function saveState() {
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify({
            stats: stats.value,
            wrongNotebook: wrongNotebook.value
          }));
        } catch(e) {
          console.error('Failed to write save:', e);
        }
      }

      // Quiz runtime state
      const quizConfig = ref({
        mode: 'unit', // 'unit' | 'exam' | 'wrong'
        unitId: 1,
        title: ''
      });
      const currentQuestions = ref([]);
      const currentQuestionIndex = ref(0);
      const userSelectedOption = ref(null);
      const answeredCurrent = ref(false);
      const examAnswers = ref({}); // { questionIndex: chosenOption }
      const startTime = ref(0);
      const elapsedSeconds = ref(0);
      let timerInterval = null;

      // Result runtime state
      const lastResult = ref({
        score: 0,
        title: '',
        correctCount: 0,
        wrongCount: 0,
        timeSpent: 0,
        wrongItems: [],
        newBadges: []
      });

      // Cards view search & filter
      const cardSearch = ref('');
      const cardFilterUnit = ref(0);

      const filteredCards = computed(() => {
        let list = ALL_QUESTIONS;
        if (cardFilterUnit.value !== 0) {
          list = list.filter(q => q.unit === cardFilterUnit.value);
        }
        if (cardSearch.value.trim()) {
          const kw = cardSearch.value.trim().toLowerCase();
          list = list.filter(q => 
            q.idiom.toLowerCase().includes(kw) || 
            q.meaning.toLowerCase().includes(kw) || 
            q.sentence.toLowerCase().includes(kw)
          );
        }
        return list;
      });

      const currentQ = computed(() => {
        return currentQuestions.value[currentQuestionIndex.value] || {};
      });

      const answeredCount = computed(() => {
        return Object.keys(examAnswers.value).length;
      });

      const unlockedBadgesCount = computed(() => {
        return Object.keys(stats.value.badges).length;
      });

      const masteredUnitsCount = computed(() => {
        return Object.values(stats.value.unitPassed).filter(Boolean).length;
      });

      // Web Audio sound generator
      function playTone(type) {
        if (!soundEnabled.value) return;
        try {
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          const ctx = new AudioContext();
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.connect(gain);
          gain.connect(ctx.destination);

          if (type === 'correct') {
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(523.25, ctx.currentTime); // C5
            osc.frequency.exponentialRampToValueAtTime(783.99, ctx.currentTime + 0.12); // G5
            gain.gain.setValueAtTime(0.2, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.25);
            osc.start();
            osc.stop(ctx.currentTime + 0.25);
          } else if (type === 'wrong') {
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(220, ctx.currentTime); // A3
            osc.frequency.setValueAtTime(180, ctx.currentTime + 0.1);
            gain.gain.setValueAtTime(0.25, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
            osc.start();
            osc.stop(ctx.currentTime + 0.3);
          } else if (type === 'fanfare') {
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(523.25, ctx.currentTime);
            osc.frequency.setValueAtTime(659.25, ctx.currentTime + 0.1);
            osc.frequency.setValueAtTime(783.99, ctx.currentTime + 0.2);
            osc.frequency.setValueAtTime(1046.50, ctx.currentTime + 0.3);
            gain.gain.setValueAtTime(0.3, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.6);
            osc.start();
            osc.stop(ctx.currentTime + 0.6);
          }
        } catch(e) {
          // AudioContext not allowed before user interaction
        }
      }

      function toggleSound() {
        soundEnabled.value = !soundEnabled.value;
      }

      // Sentence blank formatter
      function formatSentence(str) {
        if (!str) return [];
        const parts = str.split('【　　】');
        const res = [];
        parts.forEach((p, idx) => {
          if (p) res.push({ text: p, isBlank: false });
          if (idx < parts.length - 1) {
            res.push({ text: '', isBlank: true });
          }
        });
        return res;
      }

      // Format time helper (seconds -> mm:ss)
      function formatTime(sec) {
        const m = Math.floor(sec / 60);
        const s = sec % 60;
        return `${m < 10 ? '0' : ''}${m}:${s < 10 ? '0' : ''}${s}`;
      }

      // Rank titles
      function getRankTitle(score) {
        if (score === null || score === undefined) return '尚未應試';
        if (score >= 95) return '👑 成語大宗師';
        if (score >= 85) return '📜 翰林學士';
        if (score >= 70) return '⭐ 詞林進步星';
        return '🌱 勤學新秀';
      }

      // Encouragement remarks
      function getEncouragement(score) {
        if (score === 100) return '太震撼了！字字珠璣、下筆有神！您已徹底融會貫通本單元所有核心成語，表現無懈可擊！';
        if (score >= 90) return '文思泉湧、實力堅強！僅有極少數粗心細節，稍微複習一下錯題，下次必定摘下滿分榮耀！';
        if (score >= 80) return '基礎穩固、漸入佳境！對多數成語語境理解精準，將不熟的成語加入複習本，實力會更上一層樓！';
        if (score >= 60) return '及格通關！成語需要長期的浸潤與積累，建議多閱讀生活例句與錯題解析，下次定能大放異彩！';
        return '再接再厲！萬事起頭難，只要利用錯題本逐題弄懂詞義與典故，你的進步空間將會無可限量！';
      }

      // Start Mode 1: Unit Mode
      function startUnitMode(unitId) {
        const list = ALL_QUESTIONS.filter(q => q.unit === unitId);
        // Shuffle questions
        const shuffled = [...list].sort(() => Math.random() - 0.5);
        quizConfig.value = {
          mode: 'unit',
          unitId: unitId,
          title: `小單元 ${unitId} · ${unitList[unitId - 1].rowName}`
        };
        startQuizSession(shuffled);
      }

      // Start Mode 2: Exam Mode (Random 20 questions)
      function startExamMode() {
        const shuffledAll = [...ALL_QUESTIONS].sort(() => Math.random() - 0.5);
        const sample20 = shuffledAll.slice(0, 20);
        quizConfig.value = {
          mode: 'exam',
          unitId: 0,
          title: '8上第2次段考 · 綜合能力抽測 (20題)'
        };
        startQuizSession(sample20);
      }

      // Start Wrong Questions Mode
      function startWrongQuestionsQuiz() {
        if (wrongNotebook.value.length === 0) return;
        const qList = wrongNotebook.value.map(w => w.q).sort(() => Math.random() - 0.5).slice(0, 20);
        quizConfig.value = {
          mode: 'wrong',
          unitId: 0,
          title: '專屬錯題強化消滅戰'
        };
        startQuizSession(qList);
      }

      function startQuizSession(qList) {
        currentQuestions.value = qList;
        currentQuestionIndex.value = 0;
        userSelectedOption.value = null;
        answeredCurrent.value = false;
        examAnswers.value = {};
        showHint.value = false;
        showExamDrawer.value = false;
        elapsedSeconds.value = 0;
        startTime.value = Date.now();
        view.value = 'quiz';

        if (timerInterval) clearInterval(timerInterval);
        timerInterval = setInterval(() => {
          elapsedSeconds.value = Math.floor((Date.now() - startTime.value) / 1000);
        }, 1000);
      }

      // Option selection handler
      function selectOption(opt) {
        userSelectedOption.value = opt;

        if (quizConfig.value.mode === 'unit') {
          answeredCurrent.value = true;
          const isCorrect = (opt === currentQ.value.answer);
          if (isCorrect) {
            playTone('correct');
          } else {
            playTone('wrong');
            isShaking.value = true;
            setTimeout(() => { isShaking.value = false; }, 400);
            recordWrongQuestion(currentQ.value, opt);
          }
        } else {
          // Exam / Wrong Mode: store answer
          examAnswers.value[currentQuestionIndex.value] = opt;
          playTone('correct');
        }
      }

      function getOptionClass(opt) {
        if (quizConfig.value.mode === 'unit') {
          if (!answeredCurrent.value) {
            return 'bg-white hover:bg-heritage-50 border-stone-200 text-stone-800 hover:border-heritage-400';
          }
          if (opt === currentQ.value.answer) {
            return 'bg-emerald-100 border-emerald-500 text-emerald-950 font-black shadow-md';
          }
          if (userSelectedOption.value === opt) {
            return 'bg-rose-100 border-rose-500 text-rose-950 font-black';
          }
          return 'bg-stone-50 border-stone-200 text-stone-400 opacity-60';
        } else {
          // Exam mode
          const chosen = examAnswers.value[currentQuestionIndex.value];
          if (chosen === opt) {
            return 'bg-heritage-100 border-heritage-600 text-heritage-900 font-black ring-2 ring-heritage-500/50';
          }
          return 'bg-white hover:bg-stone-50 border-stone-200 text-stone-800';
        }
      }

      function nextQuestion() {
        if (currentQuestionIndex.value + 1 < currentQuestions.value.length) {
          currentQuestionIndex.value++;
          userSelectedOption.value = (quizConfig.value.mode === 'exam') ? examAnswers.value[currentQuestionIndex.value] || null : null;
          answeredCurrent.value = false;
          showHint.value = false;
        } else {
          if (quizConfig.value.mode === 'unit') {
            finishQuiz();
          } else {
            confirmSubmitExam();
          }
        }
      }

      function prevQuestion() {
        if (currentQuestionIndex.value > 0) {
          currentQuestionIndex.value--;
          userSelectedOption.value = examAnswers.value[currentQuestionIndex.value] || null;
        }
      }

      function confirmQuitQuiz() {
        if (confirm('確定要提前退出當前測驗嗎？作答進度將不會被計入。')) {
          if (timerInterval) clearInterval(timerInterval);
          view.value = 'home';
        }
      }

      function confirmSubmitExam() {
        const total = currentQuestions.value.length;
        const answered = Object.keys(examAnswers.value).length;
        if (answered < total) {
          if (!confirm(`您還有 ${total - answered} 題尚未作答！確定要現在交卷結算嗎？`)) {
            return;
          }
        }
        finishQuiz();
      }

      // Finish Quiz & Tally
      function finishQuiz() {
        if (timerInterval) clearInterval(timerInterval);
        const total = currentQuestions.value.length;
        let correctCount = 0;
        const wrongItems = [];

        currentQuestions.value.forEach((q, idx) => {
          let chosen = null;
          if (quizConfig.value.mode === 'unit') {
            chosen = q.answer; // In unit mode we already handled wrong in runtime
          } else {
            chosen = examAnswers.value[idx] || null;
          }

          if (quizConfig.value.mode === 'unit') {
            // unit mode evaluation happens in finish
            // let's evaluate directly:
          }
          if (chosen === q.answer) {
            correctCount++;
          } else {
            wrongItems.push({ q, chosen });
            recordWrongQuestion(q, chosen);
          }
        });

        // In unit mode, correctCount calculation:
        if (quizConfig.value.mode === 'unit') {
          // in unit mode, questions wrong are already tracked in wrongNotebook
          // let's calculate based on wrong count in this session
          const wrongInThis = wrongItems.length;
          correctCount = total - wrongInThis;
        }

        const score = Math.round((correctCount / total) * 100);
        const timeSpent = elapsedSeconds.value;

        // Check new badges
        const newBadges = [];
        const todayStr = new Date().toLocaleDateString('zh-TW');

        function grantBadge(bId) {
          if (!stats.value.badges[bId]) {
            stats.value.badges[bId] = { date: todayStr };
            const found = badgeList.find(b => b.id === bId);
            if (found) newBadges.push(found);
          }
        }

        if (quizConfig.value.mode === 'unit') {
          const uId = quizConfig.value.unitId;
          if (score > stats.value.unitBestScore[uId]) {
            stats.value.unitBestScore[uId] = score;
          }
          if (score >= 80) {
            stats.value.unitPassed[uId] = true;
            grantBadge(`unit_${uId}`);
          }
        } else if (quizConfig.value.mode === 'exam') {
          if (stats.value.examBestScore === null || score > stats.value.examBestScore) {
            stats.value.examBestScore = score;
          }
          if (score >= 60) grantBadge('exam_bronze');
          if (score >= 85) grantBadge('exam_silver');
          if (score === 100) grantBadge('exam_gold');
          if (timeSpent <= 120 && score >= 60) grantBadge('speed_master');
        } else if (quizConfig.value.mode === 'wrong') {
          if (score === 100) grantBadge('wrong_cleaner');
        }

        saveState();

        lastResult.value = {
          score,
          title: quizConfig.value.title,
          correctCount,
          wrongCount: total - correctCount,
          timeSpent,
          wrongItems,
          newBadges
        };

        view.value = 'result';

        if (score >= 80) {
          playTone('fanfare');
          triggerConfetti();
        }
      }

      function restartCurrentQuiz() {
        if (quizConfig.value.mode === 'unit') {
          startUnitMode(quizConfig.value.unitId);
        } else if (quizConfig.value.mode === 'exam') {
          startExamMode();
        } else {
          startWrongQuestionsQuiz();
        }
      }

      function recordWrongQuestion(q, chosen) {
        const exists = wrongNotebook.value.some(w => w.q.idiom === q.idiom);
        if (!exists) {
          wrongNotebook.value.unshift({ q, chosen, date: new Date().toLocaleDateString('zh-TW') });
          saveState();
        }
      }

      function removeSingleWrong(idx) {
        wrongNotebook.value.splice(idx, 1);
        saveState();
      }

      function clearWrongNotebook() {
        if (confirm('確定要清空整本錯題本嗎？')) {
          wrongNotebook.value = [];
          saveState();
        }
      }

      function triggerConfetti() {
        if (typeof confetti === 'function') {
          confetti({
            particleCount: 80,
            spread: 70,
            origin: { y: 0.6 }
          });
        }
      }

      function goHome() {
        if (timerInterval) clearInterval(timerInterval);
        view.value = 'home';
      }

      function exportSaveData() {
        const str = JSON.stringify({ stats: stats.value, wrongNotebook: wrongNotebook.value }, null, 2);
        const blob = new Blob([str], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `成語檢測進度存檔_${new Date().toISOString().slice(0,10)}.json`;
        a.click();
        URL.revokeObjectURL(url);
      }

      function resetAllProgress() {
        if (confirm('警告：確定要重置所有通過記錄、獎章與錯題本嗎？此操作無法撤銷！')) {
          localStorage.removeItem(STORAGE_KEY);
          stats.value = {
            unitPassed: { 1: false, 2: false, 3: false, 4: false },
            unitBestScore: { 1: 0, 2: 0, 3: 0, 4: 0 },
            examBestScore: null,
            badges: {}
          };
          wrongNotebook.value = [];
          alert('進度已全數重置為初始狀態。');
          goHome();
        }
      }

      // Keyboard shortcuts (1/2/3/4 or A/B/C/D)
      function handleKeydown(e) {
        if (view.value !== 'quiz') return;
        const key = e.key.toUpperCase();
        let idx = -1;
        if (['1', 'A'].includes(key)) idx = 0;
        if (['2', 'B'].includes(key)) idx = 1;
        if (['3', 'C'].includes(key)) idx = 2;
        if (['4', 'D'].includes(key)) idx = 3;

        if (idx >= 0 && currentQ.value.options && currentQ.value.options[idx]) {
          selectOption(currentQ.value.options[idx]);
        }
        if (e.key === 'Enter') {
          if (quizConfig.value.mode === 'unit' && answeredCurrent.value) {
            nextQuestion();
          }
        }
      }

      onMounted(() => {
        loadState();
        window.addEventListener('keydown', handleKeydown);
      });

      onUnmounted(() => {
        window.removeEventListener('keydown', handleKeydown);
        if (timerInterval) clearInterval(timerInterval);
      });

      return {
        view,
        soundEnabled,
        toggleSound,
        showHint,
        isShaking,
        showExamDrawer,
        showRoadmapModal,
        selectedBadge,
        unitList,
        badgeList,
        stats,
        wrongNotebook,
        quizConfig,
        currentQuestions,
        currentQuestionIndex,
        currentQ,
        userSelectedOption,
        answeredCurrent,
        examAnswers,
        answeredCount,
        elapsedSeconds,
        formatTime,
        formatSentence,
        getRankTitle,
        getEncouragement,
        unlockedBadgesCount,
        masteredUnitsCount,
        startUnitMode,
        startExamMode,
        startWrongQuestionsQuiz,
        selectOption,
        getOptionClass,
        nextQuestion,
        prevQuestion,
        confirmQuitQuiz,
        confirmSubmitExam,
        restartCurrentQuiz,
        lastResult,
        removeSingleWrong,
        clearWrongNotebook,
        cardSearch,
        cardFilterUnit,
        filteredCards,
        goHome,
        exportSaveData,
        resetAllProgress
      };
    }
  }).mount('#app');
</script>

</body>
</html>
"""

with open("成語大挑戰_8上第2次段考.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("成語大挑戰_8上第2次段考.html generated successfully!")
