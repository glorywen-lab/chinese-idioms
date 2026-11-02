# -*- coding: utf-8 -*-
import json

with open("debug_logs/full_all_units_database.json", "r", encoding="utf-8") as f:
    full_units = json.load(f)

html_code = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>國中成語挑戰殿堂 · Designed by 鄭汶瑜 | 壽山國中</title>
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
        <div class="flex flex-wrap items-center gap-2">
          <h1 class="text-xl sm:text-2xl font-black font-serif tracking-wide text-heritage-900">國中成語挑戰殿堂</h1>
          <span class="text-xs font-bold px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-900 border border-amber-300 shadow-sm whitespace-nowrap">Designed by 鄭汶瑜 | 壽山國中</span>
        </div>
        <p class="text-xs sm:text-sm text-heritage-700 font-semibold mt-1">
          【7上至9下 17 次段考 ＋ 其實還有】共 1,435 則成語
        </p>
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
        <span class="bg-amber-100 text-amber-800 text-xs px-1.5 py-0.5 rounded-full font-black">{{ unlockedBadgesCount }}/{{ totalBadgesCount }}</span>
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

    <!-- EXAM UNIT SWITCHER BAR -->
    <div class="glass-card rounded-2xl p-4 sm:p-5 border border-heritage-300 shadow-md">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-3">
        <div class="flex items-center gap-2">
          <span class="text-xs font-black px-2.5 py-1 rounded-md bg-heritage-700 text-white">當前測驗範圍</span>
          <h2 class="text-lg sm:text-xl font-black font-serif text-heritage-900">{{ currentUnit.name }}</h2>
        </div>
        <div class="flex items-center gap-2 text-xs text-stone-500">
          <span>範圍：{{ currentUnit.subunits[0].row_name }} ～ {{ currentUnit.subunits[currentUnit.subunits.length - 1].row_name }}</span>
          <span>•</span>
          <span class="font-bold text-heritage-800">{{ currentUnit.total_idioms }} 則成語</span>
        </div>
      </div>

      <!-- Grade Filter Tabs -->
      <div class="flex items-center gap-1.5 overflow-x-auto pb-1 mb-2 border-b border-heritage-100">
        <button 
          v-for="g in ['全部', '七年級', '八年級', '九年級', '其實還有']" 
          :key="g"
          @click="selectedGradeTab = g"
          :class="selectedGradeTab === g ? 'bg-heritage-600 text-white font-bold' : 'bg-white/80 text-stone-600 hover:bg-stone-100'"
          class="px-3 py-1 rounded-lg text-xs whitespace-nowrap transition shadow-sm">
          {{ g }}
        </button>
      </div>

      <!-- Units Grid within Grade -->
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2">
        <button 
          v-for="u in unitsInSelectedGrade" 
          :key="u.id"
          @click="switchUnit(u.id)"
          :class="currentUnitId === u.id ? 'bg-amberGold-500 text-white font-bold ring-2 ring-amberGold-400 shadow' : 'bg-white hover:bg-heritage-50 border border-heritage-200 text-stone-800'"
          class="p-2 rounded-xl text-center text-xs transition flex flex-col justify-between">
          <span class="font-bold font-serif">{{ u.name }}</span>
          <span class="text-[10px] opacity-80 mt-1">{{ u.total_idioms }} 則成語</span>
        </button>
      </div>
    </div>

    <!-- Big Banner -->
    <div class="glass-card rounded-2xl p-6 sm:p-8 border border-heritage-200/80 relative overflow-hidden">
      <div class="absolute -right-8 -bottom-8 w-48 h-48 bg-heritage-500/10 rounded-full blur-2xl pointer-events-none"></div>
      <div class="relative z-10">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-heritage-100 text-heritage-800 text-xs font-bold mb-3 border border-heritage-200">
          <span>🎯 本單元包含：{{ currentUnit.subunits.length }} 列小單元</span>
          <span>•</span>
          <span>共 {{ currentUnit.total_idioms }} 則成語</span>
          <span>•</span>
          <span class="text-emerald-700 font-extrabold">隨機多句型題庫</span>
        </div>
        <h2 class="text-2xl sm:text-3xl font-black font-serif text-heritage-900 mb-2">{{ currentUnit.name }} · 成語能力檢測</h2>
        <p class="text-stone-600 text-sm sm:text-base leading-relaxed">
          每則成語配備多組相異語境生活待答句，提供「逐列精熟學習」與「隨機抽 20 題段考模擬考」！
        </p>

        <!-- Stats Bar -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-5 border-t border-heritage-200/60">
          <div class="bg-white/60 p-3 rounded-xl border border-heritage-100">
            <div class="text-xs text-stone-500 font-medium">段考抽測最高分</div>
            <div class="text-xl font-black text-heritage-700">{{ stats.examBestScore[currentUnitId] !== undefined ? stats.examBestScore[currentUnitId] + ' 分' : '尚未測驗' }}</div>
          </div>
          <div class="bg-white/60 p-3 rounded-xl border border-heritage-100">
            <div class="text-xs text-stone-500 font-medium">本單元評定稱號</div>
            <div class="text-xl font-black text-amberGold-600">{{ getRankTitle(stats.examBestScore[currentUnitId]) }}</div>
          </div>
          <div class="bg-white/60 p-3 rounded-xl border border-heritage-100">
            <div class="text-xs text-stone-500 font-medium">小單元通關進度</div>
            <div class="text-xl font-black text-heritage-700">{{ masteredCurrentUnitSubCount }} / {{ currentUnit.subunits.length }} 單元</div>
          </div>
          <div class="bg-white/60 p-3 rounded-xl border border-heritage-100">
            <div class="text-xs text-stone-500 font-medium">全域累計勳章</div>
            <div class="text-xl font-black text-amberGold-600">{{ unlockedBadgesCount }} / {{ totalBadgesCount }} 枚</div>
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
            <span>•</span>
            <span>句式隨機不重複</span>
          </div>
          <h3 class="text-xl font-black font-serif text-heritage-900">{{ currentUnit.name }} · 綜合能力隨機抽測</h3>
          <p class="text-xs sm:text-sm text-stone-600 mt-1 leading-relaxed">
            <span>從本大單元（{{ currentUnit.total_idioms }} 則成語）中隨機挑選 20 題，</span><br>
            <span>全真模擬段考計時與作答卡，答完統一交卷結算！</span>
          </p>
        </div>
        <button @click="startExamMode" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-gradient-to-r from-amberGold-500 to-amberGold-600 hover:from-amberGold-600 hover:to-amber-700 text-white font-bold text-base shadow-md hover:shadow-lg transition flex items-center justify-center gap-2 whitespace-nowrap">
          <span>🚀 開始段考抽測</span>
          <span class="text-xs opacity-90">(20題)</span>
        </button>
      </div>
    </div>

    <!-- Mode 1: Mini Units Grid -->
    <div>
      <div class="flex items-center justify-between mb-3">
        <h3 class="text-lg font-bold font-serif text-heritage-900 flex items-center gap-2">
          <span>📚 模式一 · 逐列小單元精熟練習</span>
          <span class="text-xs font-sans font-normal text-stone-500">(以 1 列為單位 · 答對即刻反饋)</span>
        </h3>
        <button @click="view = 'cards'" class="text-xs text-heritage-600 hover:text-heritage-800 font-bold underline">
          📖 瀏覽本單元 {{ currentUnit.total_idioms }} 則成語卡
        </button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div v-for="sub in currentUnit.subunits" :key="sub.sub_id" class="glass-card rounded-xl p-5 border border-heritage-200 hover:border-heritage-500 transition group flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-black px-2.5 py-0.5 rounded-full bg-heritage-100 text-heritage-800 border border-heritage-200">
                {{ sub.title }}
              </span>
              <span v-if="stats.unitPassed[currentUnitId + '_' + sub.sub_id]" class="text-xs font-bold text-amber-600 flex items-center gap-1">
                ⭐ 最高分: {{ stats.unitBestScore[currentUnitId + '_' + sub.sub_id] }}分
              </span>
              <span v-else class="text-xs text-stone-400 font-medium">未完成</span>
            </div>
            <h4 class="text-base font-bold text-heritage-900 mb-1 group-hover:text-heritage-700 transition">
              {{ sub.row_name }} 成語精熟測驗
            </h4>
            <p class="text-xs text-stone-500 leading-relaxed mb-4">
              {{ sub.sample_idioms }}
            </p>
          </div>
          <div class="flex items-center justify-between pt-3 border-t border-heritage-100">
            <span class="text-xs text-stone-500 font-medium">全卷共 {{ sub.count }} 題</span>
            <button @click="startSubunitMode(sub.sub_id)" class="px-4 py-1.5 rounded-lg bg-heritage-700 hover:bg-heritage-800 text-white text-xs font-bold transition shadow-sm">
              {{ stats.unitPassed[currentUnitId + '_' + sub.sub_id] ? '再練一次' : '開始練習' }}
            </button>
          </div>
        </div>
      </div>
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
            {{ quizConfig.mode === 'unit' ? '模式一：逐列精熟練習' : (quizConfig.mode === 'wrong' ? '錯題消滅戰' : '模式二：段考模擬考') }}
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
        <div class="flex items-center gap-2">
          <span class="font-bold text-heritage-800">第 {{ currentQuestionIndex + 1 }} 題</span>
          <span class="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-bold">
            情境變式 #{{ (currentQ.sentenceIndex || 0) + 1 }}
          </span>
        </div>
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
          @click="currentQuestionIndex = idx; userSelectedOption = sessionAnswers[idx] || null; showExamDrawer = false"
          :class="{
            'bg-heritage-600 text-white font-bold ring-2 ring-heritage-400': currentQuestionIndex === idx,
            'bg-emerald-100 text-emerald-800 border border-emerald-300': sessionAnswers[idx] && currentQuestionIndex !== idx,
            'bg-stone-100 text-stone-600 border border-stone-200': !sessionAnswers[idx] && currentQuestionIndex !== idx
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
          🔄 換一批題目再測一次
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
            <span class="text-xs text-stone-500">{{ item.q.unit_name || currentUnit.name }}</span>
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
        <h2 class="text-2xl font-black font-serif text-heritage-900">國中三年 17 次段考 ＋ 其實還有 · 全域勳章殿堂</h2>
        <p class="text-xs sm:text-sm text-stone-500 mt-1">完成各學期段考抽測與小單元精熟，點擊勳章可查看專屬解鎖條件！</p>
      </div>
      <div class="text-right">
        <div class="text-xs text-stone-500 font-medium">總解鎖達成率</div>
        <div class="text-2xl font-black text-amberGold-600">{{ unlockedBadgesCount }} / {{ totalBadgesCount }}</div>
      </div>
    </div>

    <!-- Badge Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div 
        v-for="b in allBadgesList" 
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
        <p class="text-xs sm:text-sm text-stone-500 mt-1">跨單元集中管理各學期練習與測驗中答錯的待答句，一鍵發動消滅戰！</p>
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
      <p class="text-xs sm:text-sm text-stone-500 mb-6">您的成語掌握度極高，趕快前往段考抽測挑戰 100 分滿分金章吧！</p>
      <button @click="goHome" class="px-5 py-2.5 rounded-xl bg-heritage-700 text-white text-xs font-bold">
        返回首頁
      </button>
    </div>

    <!-- Wrong Questions List -->
    <div v-else class="space-y-4">
      <div v-for="(item, idx) in wrongNotebook" :key="idx" class="glass-card rounded-xl p-5 border border-rose-200">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-black text-rose-800 bg-rose-100 px-2 py-0.5 rounded">
            錯題 {{ idx + 1 }} · {{ item.q.unit_name || '成語檢測' }}
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
        <div class="text-xs font-bold text-heritage-600 uppercase tracking-wider mb-1">{{ currentUnit.name }} · 題庫全覽</div>
        <h2 class="text-2xl font-black font-serif text-heritage-900">{{ currentUnit.total_idioms }} 則核心成語知識卡</h2>
        <p class="text-xs sm:text-sm text-stone-500 mt-1">每則成語均包含多組生活化情境例句，點擊標籤即可自由切換預覽！</p>
      </div>
      <!-- Search Input -->
      <div class="w-full sm:w-64">
        <input v-model="cardSearch" type="text" placeholder="🔍 搜尋成語或關鍵字..." class="w-full px-3.5 py-2 rounded-xl border border-heritage-300 text-sm focus:outline-none focus:ring-2 focus:ring-heritage-500 bg-white">
      </div>
    </div>

    <!-- Filter by Subunit Tabs -->
    <div class="flex items-center gap-2 overflow-x-auto pb-2">
      <button @click="cardFilterSubunit = 0" :class="cardFilterSubunit === 0 ? 'bg-heritage-700 text-white font-bold' : 'bg-white text-stone-600 hover:bg-stone-50'" class="px-3 py-1.5 rounded-lg border border-heritage-200 text-xs whitespace-nowrap transition">
        全部 ({{ currentUnit.total_idioms }}則)
      </button>
      <button v-for="sub in currentUnit.subunits" :key="sub.sub_id" @click="cardFilterSubunit = sub.sub_id" :class="cardFilterSubunit === sub.sub_id ? 'bg-heritage-700 text-white font-bold' : 'bg-white text-stone-600 hover:bg-stone-50'" class="px-3 py-1.5 rounded-lg border border-heritage-200 text-xs whitespace-nowrap transition">
        小單元 {{ sub.sub_id }} ({{ sub.count }}則)
      </button>
    </div>

    <!-- Cards Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div v-for="q in filteredCards" :key="q.idiom" class="glass-card rounded-xl p-5 border border-heritage-200 hover:border-heritage-400 transition flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-bold text-heritage-600 bg-heritage-100 px-2 py-0.5 rounded">
              第 {{ q.row_num }} 列 · 小單元 {{ q.sub_id }}
            </span>
            <span class="text-xs text-stone-400 font-mono">{{ q.pinyin }}</span>
          </div>
          <h3 class="text-xl font-black font-serif text-heritage-900 mb-1">{{ q.idiom }}</h3>
          <p class="text-xs font-medium text-stone-600 mb-3">{{ q.meaning }}</p>

          <!-- Sentences Selector Tabs in Card -->
          <div class="p-3 rounded-lg bg-stone-50 border border-stone-200 text-xs mb-3">
            <div class="flex items-center justify-between mb-2">
              <span class="font-bold text-heritage-800">【情境待答句】</span>
              <div class="flex gap-1">
                <button 
                  v-for="(s, sIdx) in q.sentences" 
                  :key="sIdx"
                  @click="cardActiveSentence[q.idiom] = sIdx"
                  :class="(cardActiveSentence[q.idiom] || 0) === sIdx ? 'bg-heritage-700 text-white font-bold' : 'bg-white text-stone-600 hover:bg-stone-200'"
                  class="px-2 py-0.5 rounded text-[10px] border border-stone-200 transition">
                  變式 {{ sIdx + 1 }}
                </button>
              </div>
            </div>
            <div class="text-stone-800 leading-relaxed font-serif">
              {{ (q.sentences[cardActiveSentence[q.idiom] || 0] || '').replace('【　　】', '【 ' + q.idiom + ' 】') }}
            </div>
          </div>
        </div>

        <div class="text-[11px] text-stone-500 leading-relaxed pt-2 border-t border-stone-100">
          <strong class="text-stone-700">解析：</strong>{{ q.explanation }}
        </div>
      </div>
    </div>
  </main>

  <!-- ==================== FOOTER ==================== -->
  <footer class="mt-8 pt-4 border-t border-heritage-200 text-center text-xs text-stone-500 flex flex-col sm:flex-row items-center justify-between gap-2">
    <div>
      國中成語挑戰殿堂 · <strong>Designed by 鄭汶瑜 | 壽山國中</strong>
    </div>
    <div class="flex items-center gap-3">
      <button @click="exportSaveData" class="hover:underline">匯出進度</button>
      <span>•</span>
      <button @click="resetSeenSentences" class="text-emerald-700 hover:underline">重設句型防重複</button>
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

</div>

<!-- Vue 3 App Logic -->
<script>
  const ALL_UNITS_DATA = """ + json.dumps(full_units, ensure_ascii=False) + """;

  const { createApp, ref, computed, onMounted, onUnmounted } = Vue;

  createApp({
    setup() {
      // Views: 'home' | 'quiz' | 'result' | 'badges' | 'wrong_notebook' | 'cards'
      const view = ref('home');
      const soundEnabled = ref(true);
      const showHint = ref(false);
      const isShaking = ref(false);
      const showExamDrawer = ref(false);
      const selectedBadge = ref(null);
      const cardActiveSentence = ref({});

      // Selected Grade and Unit state (Default to 8上 第2次段考)
      const selectedGradeTab = ref('八年級');
      const currentUnitId = ref('8_1_2');

      const currentUnit = computed(() => {
        return ALL_UNITS_DATA[currentUnitId.value] || ALL_UNITS_DATA['8_1_2'];
      });

      const unitsInSelectedGrade = computed(() => {
        if (selectedGradeTab.value === '全部') {
          return Object.values(ALL_UNITS_DATA);
        } else if (selectedGradeTab.value === '其實還有') {
          return Object.values(ALL_UNITS_DATA).filter(u => u.name.includes('其實還有') || u.grade.includes('進階') || u.id.startsWith('extra'));
        } else {
          return Object.values(ALL_UNITS_DATA).filter(u => u.grade.includes(selectedGradeTab.value));
        }
      });

      function switchUnit(uId) {
        currentUnitId.value = uId;
        cardFilterSubunit.value = 0;
        cardSearch.value = '';
      }

      // Generate Badges List (20 units * gold/silver + milestones)
      const allBadgesList = computed(() => {
        const list = [
          { id: 'wrong_cleaner', name: '錯題清道夫', icon: '🎯', desc: '在專屬錯題消滅戰中全數答對訂正完成', condition: '完成錯題消滅戰且得分 100 分' },
          { id: 'speed_master', name: '快思敏捷', icon: '⚡', desc: '在 2 分鐘內完成段考抽測 20 題且及格', condition: '段考抽測 120 秒內完成且及格' }
        ];

        // Add badges for each unit
        for (const [uId, uObj] of Object.entries(ALL_UNITS_DATA)) {
          list.push({
            id: `gold_${uId}`,
            name: `${uObj.name}·滿貫金章`,
            icon: '🥇',
            desc: `${uObj.name} 模擬抽測榮獲 100 分滿分通關`,
            condition: `${uObj.name} 抽測滿分 100 分`
          });
          list.push({
            id: `silver_${uId}`,
            name: `${uObj.name}·拔萃銀章`,
            icon: '🥈',
            desc: `${uObj.name} 模擬抽測榮獲 85 分以上優秀成績`,
            condition: `${uObj.name} 抽測成績達 85 分以上`
          });
        }
        return list;
      });

      const totalBadgesCount = computed(() => allBadgesList.value.length);

      // Local storage persistence
      const STORAGE_KEY = 'idiom_quiz_all_grades_v4';
      const stats = ref({
        unitPassed: {},       // key: "unitId_subId": boolean
        unitBestScore: {},    // key: "unitId_subId": number
        examBestScore: {},    // key: "unitId": number
        badges: {},           // key: badgeId: { date: string }
        seenSentences: {}     // key: idiom: [indices]
      });

      const wrongNotebook = ref([]);

      function loadState() {
        try {
          const raw = localStorage.getItem(STORAGE_KEY);
          if (raw) {
            const data = JSON.parse(raw);
            if (data.stats) stats.value = Object.assign(stats.value, data.stats);
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

      // Quiz runtime
      const quizConfig = ref({
        mode: 'unit',
        unitId: '8_1_2',
        subId: 1,
        title: ''
      });
      const currentQuestions = ref([]);
      const currentQuestionIndex = ref(0);
      const userSelectedOption = ref(null);
      const answeredCurrent = ref(false);
      const sessionAnswers = ref({});
      const startTime = ref(0);
      const elapsedSeconds = ref(0);
      let timerInterval = null;

      const lastResult = ref({
        score: 0,
        title: '',
        correctCount: 0,
        wrongCount: 0,
        timeSpent: 0,
        wrongItems: [],
        newBadges: []
      });

      // Cards search & filter
      const cardSearch = ref('');
      const cardFilterSubunit = ref(0);

      const filteredCards = computed(() => {
        let list = currentUnit.value.idioms;
        if (cardFilterSubunit.value !== 0) {
          list = list.filter(q => q.sub_id === cardFilterSubunit.value);
        }
        if (cardSearch.value.trim()) {
          const kw = cardSearch.value.trim().toLowerCase();
          list = list.filter(q => 
            q.idiom.toLowerCase().includes(kw) || 
            q.meaning.toLowerCase().includes(kw) || 
            (q.sentences && q.sentences.some(s => s.toLowerCase().includes(kw)))
          );
        }
        return list;
      });

      const currentQ = computed(() => {
        return currentQuestions.value[currentQuestionIndex.value] || {};
      });

      const answeredCount = computed(() => Object.keys(sessionAnswers.value).length);
      const unlockedBadgesCount = computed(() => Object.keys(stats.value.badges).length);

      const masteredCurrentUnitSubCount = computed(() => {
        let count = 0;
        currentUnit.value.subunits.forEach(sub => {
          if (stats.value.unitPassed[`${currentUnitId.value}_${sub.sub_id}`]) count++;
        });
        return count;
      });

      // Build question instance with Unseen Sentence algorithm
      function buildQuestionInstance(idiomObj) {
        if (!stats.value.seenSentences) stats.value.seenSentences = {};
        const seenList = stats.value.seenSentences[idiomObj.idiom] || [];
        const totalVariantCount = (idiomObj.sentences && idiomObj.sentences.length > 0) ? idiomObj.sentences.length : 1;

        let available = [];
        for (let i = 0; i < totalVariantCount; i++) {
          if (!seenList.includes(i)) available.push(i);
        }

        if (available.length === 0) {
          available = Array.from({ length: totalVariantCount }, (_, i) => i);
          stats.value.seenSentences[idiomObj.idiom] = [];
        }

        const chosenIndex = available[Math.floor(Math.random() * available.length)];
        const sentence = (idiomObj.sentences && idiomObj.sentences[chosenIndex]) ? idiomObj.sentences[chosenIndex] : `請在下列句子中填入正確成語：【　　】。`;

        if (!stats.value.seenSentences[idiomObj.idiom]) stats.value.seenSentences[idiomObj.idiom] = [];
        stats.value.seenSentences[idiomObj.idiom].push(chosenIndex);

        const opts = [...(idiomObj.distractors || []), idiomObj.idiom].sort(() => Math.random() - 0.5);

        return {
          ...idiomObj,
          unit_name: currentUnit.value.name,
          sentenceIndex: chosenIndex,
          sentence: sentence,
          options: opts,
          answer: idiomObj.idiom
        };
      }

      // Audio
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
            osc.frequency.setValueAtTime(523.25, ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(783.99, ctx.currentTime + 0.12);
            gain.gain.setValueAtTime(0.2, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.25);
            osc.start();
            osc.stop(ctx.currentTime + 0.25);
          } else if (type === 'wrong') {
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(220, ctx.currentTime);
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
        } catch(e) {}
      }

      function toggleSound() {
        soundEnabled.value = !soundEnabled.value;
      }

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

      function formatTime(sec) {
        const m = Math.floor(sec / 60);
        const s = sec % 60;
        return `${m < 10 ? '0' : ''}${m}:${s < 10 ? '0' : ''}${s}`;
      }

      function getRankTitle(score) {
        if (score === null || score === undefined) return '尚未應試';
        if (score >= 95) return '👑 成語大宗師';
        if (score >= 85) return '📜 翰林學士';
        if (score >= 70) return '⭐ 詞林進步星';
        return '🌱 勤學新秀';
      }

      function getEncouragement(score) {
        if (score === 100) return '太震撼了！字字珠璣、下筆有神！您在多重語境考驗下依然表現無懈可擊，真正融會貫通！';
        if (score >= 90) return '文思泉湧、實力堅強！在不同待答句式中表現極佳，稍微留意錯題，下次必定摘下滿分金章！';
        if (score >= 80) return '基礎穩固、漸入佳境！對不同語境的理解相當到位，將不熟的成語加入複習本，實力會更上一層樓！';
        if (score >= 60) return '及格通關！成語需要長期的浸潤與積累，建議多閱讀生活例句與錯題解析，下次定能大放異彩！';
        return '再接再厲！換了新句子可能有些不適應，只要利用錯題本逐題弄懂詞義與典故，你的進步空間將會無可限量！';
      }

      // Start Mode 1: Subunit Mode
      function startSubunitMode(subId) {
        const list = currentUnit.value.idioms.filter(it => it.sub_id === subId);
        const shuffled = [...list].sort(() => Math.random() - 0.5);
        const qInstances = shuffled.map(buildQuestionInstance);
        saveState();

        const subObj = currentUnit.value.subunits.find(s => s.sub_id === subId) || { title: `小單元 ${subId}` };

        quizConfig.value = {
          mode: 'unit',
          unitId: currentUnitId.value,
          subId: subId,
          title: `${currentUnit.value.name} · ${subObj.title}`
        };
        startQuizSession(qInstances);
      }

      // Start Mode 2: Exam Mode
      function startExamMode() {
        const allIdioms = currentUnit.value.idioms;
        const shuffled = [...allIdioms].sort(() => Math.random() - 0.5);
        const sample20 = shuffled.slice(0, 20);
        const qInstances = sample20.map(buildQuestionInstance);
        saveState();

        quizConfig.value = {
          mode: 'exam',
          unitId: currentUnitId.value,
          subId: 0,
          title: `${currentUnit.value.name} · 綜合能力抽測 (20題)`
        };
        startQuizSession(qInstances);
      }

      // Start Mode 3: Wrong Questions
      function startWrongQuestionsQuiz() {
        if (wrongNotebook.value.length === 0) return;
        const qList = wrongNotebook.value.map(w => w.q).sort(() => Math.random() - 0.5).slice(0, 20);
        quizConfig.value = {
          mode: 'wrong',
          unitId: '',
          subId: 0,
          title: '專屬錯題強化消滅戰'
        };
        startQuizSession(qList);
      }

      function startQuizSession(qList) {
        currentQuestions.value = qList;
        currentQuestionIndex.value = 0;
        userSelectedOption.value = null;
        answeredCurrent.value = false;
        sessionAnswers.value = {};
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

      function selectOption(opt) {
        userSelectedOption.value = opt;
        sessionAnswers.value[currentQuestionIndex.value] = opt;

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
          const chosen = sessionAnswers.value[currentQuestionIndex.value];
          if (chosen === opt) {
            return 'bg-heritage-100 border-heritage-600 text-heritage-900 font-black ring-2 ring-heritage-500/50';
          }
          return 'bg-white hover:bg-stone-50 border-stone-200 text-stone-800';
        }
      }

      function nextQuestion() {
        if (currentQuestionIndex.value + 1 < currentQuestions.value.length) {
          currentQuestionIndex.value++;
          userSelectedOption.value = sessionAnswers.value[currentQuestionIndex.value] || null;
          answeredCurrent.value = (quizConfig.value.mode === 'unit') ? false : !!sessionAnswers.value[currentQuestionIndex.value];
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
          userSelectedOption.value = sessionAnswers.value[currentQuestionIndex.value] || null;
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
        const answered = Object.keys(sessionAnswers.value).length;
        if (answered < total) {
          if (!confirm(`您還有 ${total - answered} 題尚未作答！確定要現在交卷結算嗎？`)) {
            return;
          }
        }
        finishQuiz();
      }

      function finishQuiz() {
        if (timerInterval) clearInterval(timerInterval);
        const total = currentQuestions.value.length;
        let correctCount = 0;
        const wrongItems = [];

        currentQuestions.value.forEach((q, idx) => {
          const chosen = sessionAnswers.value[idx] || null;
          if (chosen === q.answer) {
            correctCount++;
          } else {
            wrongItems.push({ q, chosen });
            recordWrongQuestion(q, chosen);
          }
        });

        const score = Math.round((correctCount / total) * 100);
        const timeSpent = elapsedSeconds.value;

        const newBadges = [];
        const todayStr = new Date().toLocaleDateString('zh-TW');

        function grantBadge(bId) {
          if (!stats.value.badges[bId]) {
            stats.value.badges[bId] = { date: todayStr };
            const found = allBadgesList.value.find(b => b.id === bId);
            if (found) newBadges.push(found);
          }
        }

        if (quizConfig.value.mode === 'unit') {
          const key = `${quizConfig.value.unitId}_${quizConfig.value.subId}`;
          if (!stats.value.unitBestScore[key] || score > stats.value.unitBestScore[key]) {
            stats.value.unitBestScore[key] = score;
          }
          if (score >= 80) {
            stats.value.unitPassed[key] = true;
          }
        } else if (quizConfig.value.mode === 'exam') {
          const uId = quizConfig.value.unitId;
          if (!stats.value.examBestScore[uId] || score > stats.value.examBestScore[uId]) {
            stats.value.examBestScore[uId] = score;
          }
          if (score >= 85) grantBadge(`silver_${uId}`);
          if (score === 100) grantBadge(`gold_${uId}`);
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
          startSubunitMode(quizConfig.value.subId);
        } else if (quizConfig.value.mode === 'exam') {
          startExamMode();
        } else {
          startWrongQuestionsQuiz();
        }
      }

      function recordWrongQuestion(q, chosen) {
        const exists = wrongNotebook.value.some(w => w.q.idiom === q.idiom && w.q.sentenceIndex === q.sentenceIndex);
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

      function resetSeenSentences() {
        if (confirm('確定要重設句型防重複記錄嗎？所有待答句將重新從第一輪隨機出現。')) {
          stats.value.seenSentences = {};
          saveState();
          alert('已重設句型防重複記錄！');
        }
      }

      function resetAllProgress() {
        if (confirm('警告：確定要重置所有通過記錄、勳章與錯題本嗎？此操作無法撤銷！')) {
          localStorage.removeItem(STORAGE_KEY);
          stats.value = {
            unitPassed: {},
            unitBestScore: {},
            examBestScore: {},
            badges: {},
            seenSentences: {}
          };
          wrongNotebook.value = [];
          alert('進度已全數重置為初始狀態。');
          goHome();
        }
      }

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
        selectedBadge,
        cardActiveSentence,
        selectedGradeTab,
        currentUnitId,
        currentUnit,
        unitsInSelectedGrade,
        switchUnit,
        allBadgesList,
        totalBadgesCount,
        stats,
        wrongNotebook,
        quizConfig,
        currentQuestions,
        currentQuestionIndex,
        currentQ,
        userSelectedOption,
        answeredCurrent,
        sessionAnswers,
        answeredCount,
        elapsedSeconds,
        formatTime,
        formatSentence,
        getRankTitle,
        getEncouragement,
        unlockedBadgesCount,
        masteredCurrentUnitSubCount,
        startSubunitMode,
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
        cardFilterSubunit,
        filteredCards,
        goHome,
        exportSaveData,
        resetSeenSentences,
        resetAllProgress
      };
    }
  }).mount('#app');
</script>

</body>
</html>
"""

# Write to both index.html (for GitHub Pages live deploy) and 成語大挑戰_8上第2次段考.html (local primary)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_code)

with open("成語大挑戰_8上第2次段考.html", "w", encoding="utf-8") as f:
    f.write(html_code)

print("SUCCESS: index.html and 成語大挑戰_8上第2次段考.html updated successfully!")
