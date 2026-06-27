#!/usr/bin/env python3
# Build script: transforms index.html -> cul-edition.html for CUL Summer Pilot

with open('/Users/mike/fliq-100week/cul-edition.html', 'r', encoding='utf-8') as f:
    content = f.read()

errors = []

def replace(old, new):
    global content
    if old in content:
        content = content.replace(old, new)
    else:
        errors.append(f"NOT FOUND: {repr(old[:80])}")

# ─── Title / Meta ──────────────────────────────────────────────────────────

replace(
    '<title>The $100 Week™ — WealthWise Kids</title>',
    '<title>The $100 Week™ — Chicago Urban League Edition | WealthWise Kids</title>'
)

replace(
    "content=\"A 5-day behavioral finance simulation that generates your students' FLIQ Score™. No accounts. No training. No IT.\"",
    "content=\"A 4-day behavioral finance simulation — Chicago Urban League × WealthWise Kids™, Summer 2026. Powered by FLIQ Score™.\""
)

# ─── Constants ────────────────────────────────────────────────────────────

replace(
    "const SIM_ID        = 'sim_100week_v1';",
    "const SIM_ID        = 'sim_100week_cul_v1';\nconst CUL_MAX_DAYS  = 4;"
)

replace(
    "pilot_instance:'tcof_pilot_1'",
    "pilot_instance:'cul_summer_2026'"
)

# ─── Background images: Strategist days -> CUL images ─────────────────────

for d in range(1, 6):
    replace(f"url('./bg-strategist-day{d}.jpg')", f"url('./cul-day{d}.jpg')")

# ─── Day limit fixes ──────────────────────────────────────────────────────

replace("if (S.day >= 5) return;", "if (S.day >= CUL_MAX_DAYS) return;")
replace("[1,2,3,4,5].forEach(d=>{", "[1,2,3,4].forEach(d=>{")
replace("Day ${saved.day} of 5 ", "Day ${saved.day} of 4 ")
replace("if(S.day>=5){", "if(S.day>=CUL_MAX_DAYS){")
replace("if(!p.studentId||p.day<1||p.day>5) return null;",
        "if(!p.studentId||p.day<1||p.day>CUL_MAX_DAYS) return null;")

# ─── Hardcode Strategist band ─────────────────────────────────────────────

replace(
    "function startFresh(){ const band=S.band||'builder',week=S.week||1; clearProgress();",
    "function startFresh(){ const band='strategist',week=1; clearProgress();"
)

replace(
    "  screen:'home', studentId:null, sessionId:null, cohortId:null, cohortCode:null, adventureCode:null, band:'builder', week:1,",
    "  screen:'home', studentId:null, sessionId:null, cohortId:null, cohortCode:null, adventureCode:null, band:'strategist', week:1,"
)

# resetToHome hardcode
replace(
    "  const band=S.band||'builder';\n  clearProgress();\n  S={screen:'home',studentId:null,sessionId:null,cohortId:null,band,balance:getStartBal(),day:1,impulsiveN:0,history:[],profile:null,sessionStart:null,_t0:null};",
    "  const band='strategist';\n  clearProgress();\n  S={screen:'home',studentId:null,sessionId:null,cohortId:null,band,balance:getStartBal(),day:1,impulsiveN:0,history:[],profile:null,sessionStart:null,_t0:null};"
)

# ─── Hero copy ────────────────────────────────────────────────────────────

replace(
    "5 choices. Every dollar tells a story.<br>Find out what kind of money thinker you are.",
    "4 real decisions. Chicago pressure. Find out how you think with money."
)

replace("5 days, real pressure, real choices", "4 days, real pressure, real choices")

# ─── Pilot badge ─────────────────────────────────────────────────────────

replace(
    "Pilot cohorts: majority of students improved their FLIQ Score™ and demonstrated measurable gains in financial decision-making confidence.",
    "Chicago Urban League × WealthWise Kids™ — High School Financial Intelligence Pilot · Summer 2026"
)

# ─── Footer ───────────────────────────────────────────────────────────────

replace(
    "© 2026 WealthWise Kids™ LLC. All rights reserved.",
    "Chicago Urban League × WealthWise Kids™ &nbsp;·&nbsp; Powered by FLIQ Score™ &nbsp;·&nbsp; © 2026 WealthWise Kids™ LLC"
)

# ─── Feature bar ─────────────────────────────────────────────────────────

replace("3 Age Levels", "CUL Summer Pilot")
replace("Explorer · Builder · Strategist", "High School · Ages 16–18")

# ─── Band selector -> CUL partner badge ───────────────────────────────────

OLD_BAND = '''        <div class="band-selector">
          <div class="band-lbl">Who's playing?</div>
          <div class="band-pills">${bandPills}</div>
        </div>
        <div id="bandAutoNote" style="display:none;font-size:11px;color:rgba(255,255,255,0.45);margin:-6px 0 8px;text-align:center;">Your session sets this automatically.</div>'''

NEW_BAND = '''        <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.2);border-radius:14px;padding:12px 14px;margin-bottom:10px;display:flex;align-items:center;gap:12px;">
          <div style="font-size:26px;flex-shrink:0;">🏙️</div>
          <div>
            <div style="font-size:12px;font-weight:800;color:white;line-height:1.3;">Chicago Urban League</div>
            <div style="font-size:10px;color:rgba(255,255,255,0.5);margin-top:2px;letter-spacing:0.3px;">High School Financial Intelligence Pilot · Ages 16–18 · Summer 2026</div>
          </div>
        </div>'''

replace(OLD_BAND, NEW_BAND)

# ─── getDaysMeta -> CUL version ───────────────────────────────────────────

OLD_META = '''function getDaysMeta(){
  const w=S.week||1;
  if(S.band==='explorer') return w===3?DAYS_EXPLORER_W3:w===2?DAYS_EXPLORER_W2:DAYS_EXPLORER;
  if(S.band==='builder')  return w===3?DAYS_BUILDER_W3:w===2?DAYS_BUILDER_W2:DAYS_BUILDER;
  return w===3?DAYS_STRATEGIST_W3:w===2?DAYS_STRATEGIST_W2:DAYS_STRATEGIST;
}'''

NEW_META = "function getDaysMeta(){ return DAYS_CUL; }"

replace(OLD_META, NEW_META)

# ─── getScenarios -> CUL version ──────────────────────────────────────────

OLD_SCEN = '''function getScenarios(){
  const w=S.week||1;
  if(S.band==='explorer') return w===3?getExplorerScenariosW3():w===2?getExplorerScenariosW2():getExplorerScenarios();
  if(S.band==='builder')  return w===3?getBuilderScenariosW3():w===2?getBuilderScenariosW2():getBuilderScenarios();
  return w===3?getStrategistScenariosW3():w===2?getStrategistScenariosW2():getStrategistScenarios();
}'''

NEW_SCEN = "function getScenarios(){ return getCULScenarios(); }"

replace(OLD_SCEN, NEW_SCEN)

# ─── Inject DAYS_CUL + getCULScenarios after getStrategistScenarios ───────

CUL_JS = r"""
// ═══════════════════════════════════════════════════════════════
//  CUL EDITION — Chicago Urban League Summer 2026
//  4-Day Strategist Track  |  Ages 16-18
// ═══════════════════════════════════════════════════════════════

const DAYS_CUL = [
  { name:'FRIDAY',   sub:'THE DROP',  sceneCls:'sc-d1', miloImg:'./milo-happy.png',
    speech:"You've got $100 for the week.<br>Every choice shapes what comes next.<br><strong>Let's see what you do. 🎯</strong>",
    tip:"Think about what you might need before you spend today.",
    tease:"It's Friday. The crew is heading downtown. $100 in your pocket — how long does that last?",
    diLine:"Day 1. Money in hand. The first real test is already here." },
  { name:'SUNDAY',   sub:'THE ASK',   sceneCls:'sc-d2', miloImg:'./milo-concerned.png',
    speech:"Family calls different than the group chat.<br><strong>What do you do when it's personal?</strong>",
    tip:"There's a difference between giving from strength and giving from pressure. Know which one you're doing.",
    tease:"Your cousin needs something. You have it. But do you give it?",
    diLine:"Not every financial decision is about you. This one involves family." },
  { name:'MONDAY',   sub:'THE MOVE',  sceneCls:'sc-d3', miloImg:'./milo-money.png',
    speech:"A real opportunity just showed up.<br><strong>Are you ready — or does your wallet say otherwise?</strong>",
    tip:"$14/hr x 20 hrs = $280/week. What are you willing to spend to make sure you get there?",
    tease:"$14/hour is waiting. But you've gotta get there first.",
    diLine:"The opportunity showed up. The question is — did you prepare for it?" },
  { name:'THURSDAY', sub:'THE FLIP',  sceneCls:'sc-d4', miloImg:'./milo-explorer.png',
    speech:"The hustle paid off.<br><strong>What you do with it now is the whole lesson.</strong>",
    tip:"The ratio you keep — spend/save/reinvest — is the habit you're building right now.",
    tease:"You made $45. Now what? This is the real test.",
    diLine:"You made money. That's step one. Step two is what separates people who build from people who start over." },
];

function getCULScenarios() {
  const b = S.balance;
  return [
    // ── DAY 1 — THE DROP ──────────────────────────────────────────
    { day:1, scTitle:"The Crew's Weekend",
      scBody:`It's Friday. Group chat is lit — everyone's heading downtown Saturday. Navy Pier, food, maybe Regal. One of your people just got paid and is generous. Estimate: $40 easy just keeping up. You've got $100 for the week and no re-up until next Friday.`,
      visEmoji:'🌆', visCls:'vis-d1', visBadge:null,
      preChat:"No wrong answer here. <strong>But every dollar you spend today shapes the rest of the week.</strong> 🎯",
      choices:[
        { l:'A', title:"Go all in — full experience", detail:"Squad up. Food, transit, the whole thing.", cost:40, opt:'spend_social',
          costLbl:'-$40', costCls:'spend', moodLbl:'SOCIAL MOVE', moodEmoji:'👥', moodCls:'mood-social', cardCls:'type-orange', badgeCls:'badge-orange', emoji:'🌆' },
        { l:'B', title:"Go, but cap yourself at $15", detail:"Eat before you leave. Cover your own transit. Be there without over-spending.", cost:15, opt:'split_cost',
          costLbl:'-$15', costCls:'spend', moodLbl:'SMART MOVE', moodEmoji:'⚖️', moodCls:'mood-smart', cardCls:'type-teal', badgeCls:'badge-teal', emoji:'⚖️' },
        { l:'C', title:"Pass this weekend. Put $20 toward something.", detail:"FOMO is real. But so is having a plan.", cost:0, opt:'save',
          costLbl:`Keep $${b}`, costCls:'save', moodLbl:'HOLD MOVE', moodEmoji:'🎯', moodCls:'mood-safe', cardCls:'type-green', badgeCls:'badge-green', emoji:'🎯' },
      ],
      outcome(c){
        if(c===0) return { cls:'neg', title:"You showed up.", text:`Nothing wrong with showing up for your people. But $40 on Saturday means $60 for the rest of the week — and something always comes up. Keep that in the back of your head.` };
        if(c===1) return { cls:'pos', title:"You capped yourself.", text:`Smart play. You were still there, still present. And you kept $${b-15} for the week. Nobody even noticed the difference.` };
        return          { cls:'pos', title:"You passed.", text:`FOMO is real. But so is having $100 next week when everyone else is broke. What are you building toward?` };
      },
      milo(c){
        if(c===0) return { img:'./milo-concerned.png', txt:`$40 on Saturday means $60 for the whole week. Something always comes up — hope you're ready. 👀` };
        if(c===1) return { img:'./milo-happy.png',     txt:"You were still there, still in the moment. And you kept $85 for the week. That's the move. 🎯" };
        return          { img:'./milo-proud.png',      txt:"FOMO is real. But so is having a plan. What are you building toward? 💪" };
      },
    },
    // ── DAY 2 — THE ASK ───────────────────────────────────────────
    { day:2, scTitle:"Family First",
      scBody: priorChoice(1)===0
        ? `Sunday morning. You spent $40 on Saturday — down to <strong>$${b}</strong>. Your little cousin needs $20 for a school supply run. Their mom says she'll pay you back "when she gets it." You know how that goes. But it's your cousin. And school starts Monday.`
        : priorChoice(1)===1
        ? `Sunday morning. You kept it tight Saturday — you have $${b}. Your little cousin needs $20 for a school supply run. Their mom says she'll pay you back "when she gets it." But it's your cousin. And school starts Monday.`
        : `Sunday morning. You held your money Saturday — still sitting on $${b}. Your little cousin needs $20 for school supplies. Their mom says she'll pay you back. But it's your cousin. School starts Monday.`,
      visEmoji:'🏘️', visCls:'vis-d2', visBadge:null,
      preChat: b < 60
        ? `You're already down from Saturday. <strong>Is $20 something you can give right now?</strong> 🏘️`
        : "Family is family. <strong>But this is still a financial decision.</strong> Think it through. 🏘️",
      choices:[
        { l:'A', title:"Give the $20 — family is family", detail:"You cover it. No hesitation.", cost:20, opt:'spend_social',
          costLbl:'-$20', costCls:'spend', moodLbl:'FAMILY MOVE', moodEmoji:'❤️', moodCls:'mood-social', cardCls:'type-blue', badgeCls:'badge-blue', emoji:'❤️' },
        { l:'B', title:"Give $10 — split the difference", detail:"You cover half. They figure out the rest.", cost:10, opt:'give_partial',
          costLbl:'-$10', costCls:'spend', moodLbl:'BALANCED', moodEmoji:'⚖️', moodCls:'mood-smart', cardCls:'type-teal', badgeCls:'badge-teal', emoji:'⚖️' },
        { l:'C', title:"Take your cousin to the dollar store yourself", detail:"Go with them. Pay directly so the money doesn't disappear into the household.", cost:12, opt:'give_noncash',
          costLbl:'-~$12', costCls:'spend', moodLbl:'SMART GIVE', moodEmoji:'🛒', moodCls:'mood-smart', cardCls:'type-purple', badgeCls:'badge-purple', emoji:'🛒' },
      ],
      outcome(c){
        if(c===0) return { cls:'neu', title:"You showed up for family.", text:`Respect. You gave $20 when it mattered. Just know — "I'll pay you back" has a track record in every household. Was it worth it? Probably. Will you get it back? Different question.` };
        if(c===1) return { cls:'pos', title:"You covered what you could.", text:`You showed up without over-extending. Your cousin has something to work with and you kept your cushion. That's not cold — that's responsible for both of you.` };
        return          { cls:'pos', title:"Smartest play in the room.", text:`Your cousin gets exactly what they need. The money doesn't disappear into the household. And you stayed in control. Financial AND relational intelligence — at the same time.` };
      },
      milo(c){
        if(c===0) return { img:'./milo-smile.png',     txt:"You showed up for family. Respect. Just track whether that $20 comes back — not for the money, but for the pattern. 💙" };
        if(c===1) return { img:'./milo-happy.png',     txt:"You showed up without over-extending yourself. Your cousin has something. You kept your cushion. Balance. ⚖️" };
        return          { img:'./milo-explorer.png',   txt:"That's the smartest play in the room. Controlled the outcome AND helped your cousin. Financial AND relational intelligence. 🎯" };
      },
    },
    // ── DAY 3 — THE MOVE ──────────────────────────────────────────
    { day:3, scTitle:"Your Time Is Coming",
      scBody: (priorChoice(1)===0 && b < 50)
        ? `Monday. You've been spending — down to <strong>$${b}</strong>. But you scored a callback interview downtown: part-time logistics job, $14/hour, 20 hours a week. Interview is Thursday. Your transit card is empty. A month reload is $30. You've got class and practice before then. Rides aren't guaranteed.`
        : `Monday. You scored a callback interview at a logistics company downtown — $14/hour, 20 hours a week. Interview is Thursday. Problem: your transit card is empty. Full month reload is $30. You've got class and practice in between. You could ask around for rides, but nothing's guaranteed.`,
      visEmoji:'🚂', visCls:'vis-d3', visBadge:'$14/hr',
      preChat: b < 40
        ? `You're running low — and this interview could change everything. <strong>Do the math before you decide.</strong> 🚂`
        : "<strong>$14/hr × 20 hrs = $280/week.</strong> What are you willing to spend to make sure you get there? 🚂",
      choices:[
        { l:'A', title:"Load the transit card now — all $30", detail:"You're not leaving this to chance. That interview is Thursday.", cost:30, opt:'spend_essential',
          costLbl:'-$30', costCls:'spend', moodLbl:'LOCK IT IN', moodEmoji:'🎯', moodCls:'mood-safe', cardCls:'type-teal', badgeCls:'badge-teal', emoji:'🚂' },
        { l:'B', title:"Line up 3 rides first — load the card Wednesday if needed", detail:"Work the network. Only fall back on the card if rides fall through by Wednesday.", cost:0, opt:'defer_decision',
          costLbl:'-$0 now', costCls:'save', moodLbl:'CONTINGENCY', moodEmoji:'📋', moodCls:'mood-smart', cardCls:'type-purple', badgeCls:'badge-purple', emoji:'📋' },
        { l:'C', title:"Day pass only — morning of the interview", detail:"$5 the morning of. Stretch the rest of the week on foot and rides.", cost:5, opt:'spend_frugal',
          costLbl:'-$5 Thursday', costCls:'spend', moodLbl:'TIGHT TACTIC', moodEmoji:'⚡', moodCls:'mood-smart', cardCls:'type-orange', badgeCls:'badge-orange', emoji:'⚡' },
      ],
      outcome(c){
        if(c===0) return { cls:'pos', title:"You locked it in.", text:`$14/hour × 20 hours = $280 a week. You spent $30 to protect access to that. That's not spending — that's investing in yourself. Do the math every time.` };
        if(c===1) return { cls:'neu', title:"Smart contingency.", text:`Working the network first is smart. But lock your backup down by Tuesday — not Wednesday night. Interviews don't reschedule for transit problems.` };
        return          { cls:'pos', title:"Tight but tactical.", text:`You protected the one day that mattered without locking $30 out of reach for the month. Just make sure that day pass is confirmed — not assumed — the night before.` };
      },
      milo(c){
        if(c===0) return { img:'./milo-encouraging.png', txt:"Non-negotiable. $280/week opportunity. You spent $30 to protect it. That's not an expense — that's a return on investment. 📈" };
        if(c===1) return { img:'./milo-thinking.png',    txt:"Smart contingency play. But have your backup locked by Tuesday. Interviews don't reschedule for anyone. ⚡" };
        return          { img:'./milo-happy.png',        txt:"Tight and tactical. You kept cash free and protected the interview. Just confirm that day pass the night before — not the morning of. 🎯" };
      },
    },
    // ── DAY 4 — THE FLIP ──────────────────────────────────────────
    { day:4, scTitle:"Hustle Paid Off",
      scBody:`Thursday evening. The interview went well — they'll be in touch next week. Also: your side hustle (selling snacks and drinks at school) pulled in $45 this week. You're holding more cash than you've had at one time in a minute. What do you do with the $45 you earned?`,
      visEmoji:'💸', visCls:'vis-d4', visBadge:'+$45',
      preChat:"You earned it — that's real. <strong>What you do with it now is the whole lesson.</strong> 💸",
      choices:[
        { l:'A', title:"Treat yourself — you earned it", detail:"New fit, a dinner out, whatever feels right. You worked for this. ($45 spent)", cost:45, opt:'spend_nonessential',
          costLbl:'-$45', costCls:'spend', moodLbl:'REWARD MOVE', moodEmoji:'🎁', moodCls:'mood-social', cardCls:'type-orange', badgeCls:'badge-orange', emoji:'🎁' },
        { l:'B', title:"Split it: $20 reinvest, $15 save, $10 spend", detail:"Put money back into the hustle. Hold some. Reward yourself a little.", cost:10, opt:'invest_partial',
          costLbl:'$10 spend', costCls:'spend', moodLbl:'BUSINESS MOVE', moodEmoji:'📊', moodCls:'mood-smart', cardCls:'type-teal', badgeCls:'badge-teal', emoji:'📊' },
        { l:'C', title:"Put all $45 somewhere you won't touch it", detail:"Call it your first-move fund. Leave it alone until the right moment.", cost:0, opt:'save',
          costLbl:'Save $45', costCls:'save', moodLbl:'STACK MOVE', moodEmoji:'🏦', moodCls:'mood-safe', cardCls:'type-green', badgeCls:'badge-green', emoji:'🏦' },
      ],
      outcome(c){
        if(c===0) return { cls:'neu', title:"You treated yourself.", text:`You worked for it — that's real. But here's the question: what ratio do you want to live by? Spend it all every time, or build toward something? The hustle comes back next week. The ratio is what compounds.` };
        if(c===1) return { cls:'pos', title:"That's the business owner's brain.", text:`Reinvest, reserve, reward — in that order. You just ran a profit-and-loss decision on a school hallway hustle. That's not small. Keep that ratio and you're building something real.` };
        return          { cls:'pos', title:"You stacked it.", text:`You turned a side hustle into a savings event. That's the most disciplined play of the week. What's the first move when that fund hits $200? Because it will — if you stay consistent.` };
      },
      milo(c){
        if(c===0) return { img:'./milo-smile.png',     txt:"You worked for it. Spending it isn't a crime. But what ratio do you want to live by? That answer tells you everything. 🎯" };
        if(c===1) return { img:'./milo-explorer.png',  txt:"Reinvest, reserve, reward — in that order. You just ran a business decision in a high school hallway. That ratio is the whole game. 📊" };
        return          { img:'./milo-proud.png',      txt:"Stacked the whole $45. That's discipline. What's the first move when it hits $200? Because it will — if you stay consistent. 🏦" };
      },
    },
  ];
}
"""

marker = "} // end getStrategistScenarios"
if marker in content:
    content = content.replace(marker, marker + "\n" + CUL_JS)
else:
    errors.append("NOT FOUND: getStrategistScenarios end marker")

# ─── Write result ─────────────────────────────────────────────────────────

with open('/Users/mike/fliq-100week/cul-edition.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nBuild complete. {len(errors)} error(s):")
for e in errors:
    print(f"  ✗ {e}")
if not errors:
    print("  All replacements applied successfully.")
