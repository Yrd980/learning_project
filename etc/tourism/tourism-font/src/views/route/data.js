const coordData = [
    {
        name: '黑龙江',
        position: [127, 47],
        pointData: {
            out: 100,
            provide: 10,
        },
        line: [
            {
                current: [
                    [127, 47],
                    [126, 43],
                ],
                type: 1,
            },
        ],
    },
    {
        name: '吉林',
        position: [126, 43],
        pointData: {
            out: 120,
            provide: 11,
        },
        line: [
            {
                current: [
                    [126, 43],
                    [113, 41],
                ],
                type: 1,
            },
        ],
    },
]

const attractionData = [
    {
        id: 1,
        name: "东方明珠塔",
        description: "东方明珠广播电视塔是上海的标志性文化景观之一，塔高约468米。",
        image: "https://example.com/image/oriental_pearl_tower.jpg",
        position: [121.4737, 31.2304], // 经度, 纬度
    },
    {
        id: 2,
        name: "外滩",
        description: "外滩位于黄浦江畔，是最具上海特色的欧式建筑群，是上海的标志。",
        image: "https://example.com/image/bund.jpg",
        position: [121.4957, 31.2304],
    },
    {
        id: 3,
        name: "豫园",
        description: "豫园是明代的一座私人园林，现在是上海著名的旅游景点。",
        image: "https://example.com/image/yu_garden.jpg",
        position: [121.4833, 31.2222],
    },
]

const routeLine = [
    [121.4737, 31.2304],
    [121.4957, 31.2304],
    [121.4833, 31.2222]
]
export {
    coordData, attractionData,routeLine
}
