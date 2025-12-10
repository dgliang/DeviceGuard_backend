import { defineGkdApp } from '@gkd-kit/define';

export default defineGkdApp({
  id: 'com.xunmeng.pinduoduo',
  name: '拼多多',
  groups: [
    {
      key: 0,
      name: 'in-app|0mgbwEwu5whS3Oa1twLiTctmrLB0rcyVT5UwH_gIIvI=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '',
          matches:
            'android.widget.FrameLayout > android.widget.LinearLayout > android.widget.FrameLayout[id="android:id/content"] > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.LinearLayout[id="com.xunmeng.pinduoduo:id/pdd"][clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 1,
      name: 'in-app|4cwZug9yJOoulaxafQK-J-ZrlHbwVmAiIBWnCJIS4n8=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '.app_address_lego.CreateLegoAddressActivity',
          matches:
            'android.widget.FrameLayout > android.widget.LinearLayout > android.widget.FrameLayout[id="android:id/content"] > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout > android.view.ViewGroup[id="com.xunmeng.pinduoduo:id/pdd"] > android.view.ViewGroup > android.view.ViewGroup[clickable=true] > android.view.ViewGroup > android.widget.ImageView[desc="关闭"][clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 2,
      name: 'in-app|4dHWQ_lIgF3yspSa-6_6sYsSA_bOy_ipju4oiH2i3cs=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '',
          matches:
            'android.widget.FrameLayout > android.widget.LinearLayout > android.widget.FrameLayout[id="android:id/content"] > android.widget.LinearLayout > android.view.ViewGroup[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.TextView[id="com.xunmeng.pinduoduo:id/pdd"][text=""][clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 3,
      name: 'in-app|76QB7TBdBNLoerNRTFr4BQN2W8Wpe7rGaIkzLD3lorE=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '.app_address_lego.CreateLegoAddressActivity',
          matches:
            'android.widget.FrameLayout > android.widget.LinearLayout > android.widget.FrameLayout[id="android:id/content"] > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout > android.view.ViewGroup[id="com.xunmeng.pinduoduo:id/pdd"] > android.view.ViewGroup > android.view.ViewGroup[clickable=true] > android.view.ViewGroup > android.view.ViewGroup > android.view.ViewGroup > android.view.ViewGroup > android.widget.ImageView[desc="清空收货人姓名"][clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 4,
      name: 'in-app|aKGWXOl7-0D9bHtAEagU3Pr_Rx9k9h51CbinWKGl5F8=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '.activity.NewPageMaskActivity',
          matches:
            'android.widget.FrameLayout > android.widget.LinearLayout > android.widget.FrameLayout[id="android:id/content"] > android.widget.FrameLayout > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout > android.view.ViewGroup[id="com.xunmeng.pinduoduo:id/pdd"] > android.view.ViewGroup > android.view.ViewGroup[clickable=true] > android.view.ViewGroup[clickable=true] > android.view.ViewGroup > android.view.ViewGroup > android.view.ViewGroup[clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 5,
      name: 'in-app|EpmAc53r2SQOpW10Di0s1eOx9yLbxOJCwxrdwK1Hm4g=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '.ui.activity.MainFrameActivity',
          matches:
            'android.widget.FrameLayout[desc="拍照搜索"] > android.widget.FrameLayout > android.widget.FrameLayout > android.widget.FrameLayout > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout > android.view.ViewGroup[id="com.xunmeng.pinduoduo:id/pdd"] > android.view.ViewGroup[clickable=true] > android.view.ViewGroup[clickable=true] > android.view.ViewGroup[clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 6,
      name: 'in-app|Gqn_t3SQEm598_wwTG-xa2_cQUeAJDQhWTCvoOci2bM=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '',
          matches:
            'android.widget.FrameLayout > android.widget.LinearLayout > android.widget.FrameLayout[id="android:id/content"] > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.LinearLayout[id="com.xunmeng.pinduoduo:id/pdd"][clickable=true] > android.view.ViewGroup[id="com.xunmeng.pinduoduo:id/pdd"][clickable=true] > android.widget.LinearLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.view.ViewGroup > android.widget.LinearLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.RelativeLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.view.ViewGroup[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.LinearLayout[id="com.xunmeng.pinduoduo:id/gnl"] > android.widget.LinearLayout > android.widget.ImageView[id="com.xunmeng.pinduoduo:id/pdd"][desc="增加数量"][clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 7,
      name: 'in-app|gTFUAJ5Vr6BNbDxpPAqAm8ez1A4CZ6HStqu9Yf_pF00=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '.app_address_lego.CreateLegoAddressActivity',
          matches:
            'android.widget.FrameLayout > android.widget.FrameLayout > android.widget.FrameLayout[id="android:id/content"] > android.view.ViewGroup > android.view.ViewGroup > android.view.ViewGroup > android.view.ViewGroup[clickable=true] > android.view.ViewGroup > android.view.ViewGroup[clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 8,
      name: 'in-app|jvxQH-Ay3iPbSfyt54vVXJcPjljEoqCQ1T482mLFrig=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '.activity.NewPageActivity',
          matches:
            'android.widget.FrameLayout[desc="返回"] > android.widget.FrameLayout > android.widget.FrameLayout > android.widget.FrameLayout > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout > android.view.ViewGroup[id="com.xunmeng.pinduoduo:id/pdd"] > android.view.ViewGroup > android.view.ViewGroup[clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 9,
      name: 'in-app|LFDmyJyhtJodjrgUMYbLd6sH97WN9P4AWkc_Cue4SRA=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '',
          matches:
            'android.widget.FrameLayout > android.widget.FrameLayout > android.widget.FrameLayout[id="android:id/content"] > android.widget.FrameLayout > android.view.View[id="com.xunmeng.pinduoduo:id/pdd"][desc="关闭"][clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 10,
      name: 'in-app|MXKZCPhB1os78JslWKnxOJUU2FWZz0ASefC47LP0kQI=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '.app_address_lego.CreateLegoAddressActivity',
          matches:
            'android.widget.FrameLayout > android.widget.LinearLayout > android.widget.FrameLayout[id="android:id/content"] > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout > android.view.ViewGroup[id="com.xunmeng.pinduoduo:id/pdd"] > android.view.ViewGroup > android.view.ViewGroup[clickable=true] > android.view.ViewGroup > android.view.ViewGroup > android.view.ViewGroup > android.view.ViewGroup > android.widget.ImageView[desc="清空收货人姓名"][clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 11,
      name: 'in-app|o3qoOEmKh5hJtg_y6U5L3U4_WGe_4rU4D9AmS62zy-0=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '.activity.NewPageMaskActivity',
          matches:
            'android.widget.FrameLayout > android.widget.LinearLayout > android.widget.FrameLayout[id="android:id/content"] > android.widget.FrameLayout > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout > android.view.ViewGroup[id="com.xunmeng.pinduoduo:id/pdd"] > android.view.ViewGroup > android.view.ViewGroup[clickable=true] > android.view.ViewGroup[clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 12,
      name: 'in-app|opbylGqvXufWm1lwldViepIXStGiAwPtLUt1YUuNk_0=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '.app_address_lego.CreateLegoAddressActivity',
          matches:
            'android.widget.FrameLayout > android.widget.LinearLayout > android.widget.FrameLayout[id="android:id/content"] > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout > android.view.ViewGroup[id="com.xunmeng.pinduoduo:id/pdd"] > android.view.ViewGroup > android.view.ViewGroup[clickable=true] > android.view.ViewGroup > android.widget.ImageView[desc="关闭"][clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 13,
      name: 'in-app|SkoZeoRgec_49oG2Ti568k9EPMDl-f-hWshZ2Xhaw8M=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '.activity.NewPageActivity',
          matches:
            'android.widget.FrameLayout[desc="返回"] > android.widget.FrameLayout > android.widget.FrameLayout > android.widget.FrameLayout > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout > android.view.ViewGroup[id="com.xunmeng.pinduoduo:id/pdd"] > android.view.ViewGroup > android.view.ViewGroup > android.view.ViewGroup > android.widget.FrameLayout[clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 14,
      name: 'in-app|T_vWDaSxFkfBnoHTJyAfX_IKFq7u44tFswnwFDAEa9c=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '.activity.NewPageActivity',
          matches:
            'android.widget.FrameLayout[desc="返回"] > android.widget.FrameLayout > android.widget.FrameLayout > android.widget.FrameLayout > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout > android.view.ViewGroup[id="com.xunmeng.pinduoduo:id/pdd"] > android.view.ViewGroup > android.view.ViewGroup[clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 15,
      name: 'in-app|y7skzrl6UoWC0Y6_h45vqHi-C-3YqAYCEOgcvTbgoVU=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '.app_address_lego.CreateLegoAddressActivity',
          matches:
            'android.widget.FrameLayout > android.widget.LinearLayout > android.widget.FrameLayout[id="android:id/content"] > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout > android.view.ViewGroup[id="com.xunmeng.pinduoduo:id/pdd"] > android.view.ViewGroup > android.view.ViewGroup[clickable=true] > android.view.ViewGroup > android.widget.ImageView[desc="关闭"][clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 16,
      name: 'in-app|ZCk_wtXcH1hnS0duvvuxgOcHcOcIjM1TrPv658DipL8=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '.activity.NewPageMaskActivity',
          matches:
            'android.widget.FrameLayout > android.widget.LinearLayout > android.widget.FrameLayout[id="android:id/content"] > android.widget.FrameLayout > android.widget.FrameLayout[id="com.xunmeng.pinduoduo:id/pdd"] > android.widget.FrameLayout > android.view.ViewGroup[id="com.xunmeng.pinduoduo:id/pdd"] > android.view.ViewGroup > android.view.ViewGroup[clickable=true] > android.view.ViewGroup[clickable=true] > android.view.ViewGroup[clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
    {
      key: 17,
      name: 'in-app|zO1fiM-E2RoZgdtTnSUcClJG7IYhnptULDDzgh7sa1w=.png',
      actionDelay: 3000,
      actionMaximum: 3,
      resetMatch: 'app',
      priorityTime: 10000,
      matchRoot: true,
      rules: [
        {
          action: 'clickCenter',
          activityIds: '',
          matches:
            'android.widget.FrameLayout > android.widget.FrameLayout > android.widget.FrameLayout[id="android:id/content"] > android.widget.FrameLayout > android.view.View[id="com.xunmeng.pinduoduo:id/pdd"][desc="关闭"][clickable=true]',
          snapshotUrls: 'https://i.gkd.li/i/13183946',
        },
      ],
    },
  ],
});
