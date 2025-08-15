// Food & Calories Guide JavaScript
// Comprehensive food database with 50+ items

// Food Database with accurate nutritional information
const foodDatabase = [
    // PROTEINS
    {
        id: 1,
        name: "صدر الدجاج",
        nameEn: "Chicken Breast",
        category: "protein",
        calories: 165,
        protein: 31,
        carbs: 0,
        fat: 3.6,
        image: "🐔",
        tags: ["عالي البروتين", "قليل الدهون", "صديق الكيتو"],
        tagClasses: ["tag-protein", "tag-keto", "tag-protein"],
        icons: ["🥗", "🥩"],
        note: "مصدر ممتاز للبروتين عالي الجودة، مثالي لبناء العضلات",
        goals: ["muscle_gain", "weight_loss"],
        calorieLevel: "medium"
    },
    {
        id: 2,
        name: "لحم البقر الخالي من الدهن",
        nameEn: "Lean Beef",
        category: "protein",
        calories: 250,
        protein: 26,
        carbs: 0,
        fat: 15,
        image: "🥩",
        tags: ["عالي البروتين", "غني بالحديد", "صديق الكيتو"],
        tagClasses: ["tag-protein", "tag-protein", "tag-keto"],
        icons: ["🥩", "💪"],
        note: "مصدر غني بالبروتين والحديد والزنك",
        goals: ["muscle_gain"],
        calorieLevel: "high"
    },
    {
        id: 3,
        name: "سلمون",
        nameEn: "Salmon",
        category: "protein",
        calories: 208,
        protein: 22,
        carbs: 0,
        fat: 12,
        image: "🐟",
        tags: ["أوميغا 3", "عالي البروتين", "صحي للقلب"],
        tagClasses: ["tag-protein", "tag-protein", "tag-vegan"],
        icons: ["🥩", "❤️"],
        note: "غني بأحماض أوميغا 3 الدهنية المفيدة للقلب والدماغ",
        goals: ["muscle_gain", "maintenance"],
        calorieLevel: "medium"
    },
    {
        id: 4,
        name: "تونة",
        nameEn: "Tuna",
        category: "protein",
        calories: 144,
        protein: 30,
        carbs: 0,
        fat: 1,
        image: "🐟",
        tags: ["عالي البروتين", "قليل الدهون", "اقتصادي"],
        tagClasses: ["tag-protein", "tag-keto", "tag-budget"],
        icons: ["🥗", "🥩"],
        note: "بروتين عالي الجودة وقليل السعرات، مثالي لفقدان الوزن",
        goals: ["weight_loss", "muscle_gain"],
        calorieLevel: "low"
    },
    {
        id: 5,
        name: "بيض",
        nameEn: "Eggs",
        category: "protein",
        calories: 155,
        protein: 13,
        carbs: 1.1,
        fat: 11,
        image: "🥚",
        tags: ["بروتين كامل", "فيتامينات", "اقتصادي"],
        tagClasses: ["tag-protein", "tag-protein", "tag-budget"],
        icons: ["🥩", "💰"],
        note: "يحتوي على جميع الأحماض الأمينية الأساسية",
        goals: ["muscle_gain", "maintenance"],
        calorieLevel: "medium"
    },
    {
        id: 6,
        name: "جبن قريش",
        nameEn: "Cottage Cheese",
        category: "protein",
        calories: 98,
        protein: 11,
        carbs: 3.4,
        fat: 4.3,
        image: "🧀",
        tags: ["عالي البروتين", "قليل السعرات", "كالسيوم"],
        tagClasses: ["tag-protein", "tag-keto", "tag-protein"],
        icons: ["🥗", "🦴"],
        note: "مصدر ممتاز للبروتين والكالسيوم",
        goals: ["weight_loss", "muscle_gain"],
        calorieLevel: "low"
    },
    {
        id: 7,
        name: "عدس",
        nameEn: "Lentils",
        category: "protein",
        calories: 116,
        protein: 9,
        carbs: 20,
        fat: 0.4,
        image: "🫘",
        tags: ["نباتي", "عالي الألياف", "اقتصادي"],
        tagClasses: ["tag-vegan", "tag-fiber", "tag-budget"],
        icons: ["🌱", "💰"],
        note: "مصدر نباتي ممتاز للبروتين والألياف",
        goals: ["weight_loss", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 8,
        name: "حمص",
        nameEn: "Chickpeas",
        category: "protein",
        calories: 164,
        protein: 8.9,
        carbs: 27,
        fat: 2.6,
        image: "🫛",
        tags: ["نباتي", "عالي الألياف", "اقتصادي"],
        tagClasses: ["tag-vegan", "tag-fiber", "tag-budget"],
        icons: ["🌱", "💰"],
        note: "غني بالبروتين النباتي والألياف والفولات",
        goals: ["weight_loss", "maintenance"],
        calorieLevel: "medium"
    },
    {
        id: 9,
        name: "فول الصويا",
        nameEn: "Soybeans",
        category: "protein",
        calories: 173,
        protein: 16.6,
        carbs: 9.9,
        fat: 9,
        image: "🫘",
        tags: ["نباتي", "بروتين كامل", "إيزوفلافون"],
        tagClasses: ["tag-vegan", "tag-protein", "tag-vegan"],
        icons: ["🌱", "🥩"],
        note: "البروتين النباتي الوحيد الذي يحتوي على جميع الأحماض الأمينية",
        goals: ["muscle_gain", "maintenance"],
        calorieLevel: "medium"
    },

    // CARBOHYDRATES
    {
        id: 10,
        name: "شوفان",
        nameEn: "Oats",
        category: "carbs",
        calories: 389,
        protein: 16.9,
        carbs: 66,
        fat: 6.9,
        image: "🌾",
        tags: ["عالي الألياف", "بطيء الهضم", "صحي للقلب"],
        tagClasses: ["tag-fiber", "tag-fiber", "tag-vegan"],
        icons: ["❤️", "⏰"],
        note: "كربوهيدرات معقدة توفر طاقة مستدامة",
        goals: ["muscle_gain", "maintenance"],
        calorieLevel: "high"
    },
    {
        id: 11,
        name: "أرز بني",
        nameEn: "Brown Rice",
        category: "carbs",
        calories: 111,
        protein: 2.6,
        carbs: 23,
        fat: 0.9,
        image: "🍚",
        tags: ["حبوب كاملة", "عالي الألياف", "اقتصادي"],
        tagClasses: ["tag-fiber", "tag-fiber", "tag-budget"],
        icons: ["🌾", "💰"],
        note: "مصدر ممتاز للكربوهيدرات المعقدة والألياف",
        goals: ["muscle_gain", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 12,
        name: "كينوا",
        nameEn: "Quinoa",
        category: "carbs",
        calories: 120,
        protein: 4.4,
        carbs: 22,
        fat: 1.9,
        image: "🌾",
        tags: ["بروتين كامل", "خالي من الجلوتين", "سوبرفود"],
        tagClasses: ["tag-protein", "tag-vegan", "tag-vegan"],
        icons: ["🌱", "⭐"],
        note: "حبوب فائقة الجودة تحتوي على بروتين كامل",
        goals: ["muscle_gain", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 13,
        name: "خبز القمح الكامل",
        nameEn: "Whole Wheat Bread",
        category: "carbs",
        calories: 247,
        protein: 13,
        carbs: 41,
        fat: 4.2,
        image: "🍞",
        tags: ["حبوب كاملة", "عالي الألياف", "اقتصادي"],
        tagClasses: ["tag-fiber", "tag-fiber", "tag-budget"],
        icons: ["🌾", "💰"],
        note: "مصدر جيد للكربوهيدرات المعقدة والألياف",
        goals: ["maintenance"],
        calorieLevel: "high"
    },
    {
        id: 14,
        name: "مكرونة القمح الكامل",
        nameEn: "Whole Wheat Pasta",
        category: "carbs",
        calories: 124,
        protein: 5,
        carbs: 25,
        fat: 1.1,
        image: "🍝",
        tags: ["حبوب كاملة", "عالي الألياف", "طاقة مستدامة"],
        tagClasses: ["tag-fiber", "tag-fiber", "tag-vegan"],
        icons: ["🌾", "⚡"],
        note: "كربوهيدرات معقدة مثالية قبل التمرين",
        goals: ["muscle_gain", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 15,
        name: "موز",
        nameEn: "Banana",
        category: "carbs",
        calories: 89,
        protein: 1.1,
        carbs: 23,
        fat: 0.3,
        image: "🍌",
        tags: ["طاقة سريعة", "بوتاسيوم", "طبيعي"],
        tagClasses: ["tag-vegan", "tag-vegan", "tag-vegan"],
        icons: ["⚡", "🏃"],
        note: "مثالي قبل وبعد التمرين لتجديد الطاقة",
        goals: ["muscle_gain", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 16,
        name: "تفاح",
        nameEn: "Apple",
        category: "carbs",
        calories: 52,
        protein: 0.3,
        carbs: 14,
        fat: 0.2,
        image: "🍎",
        tags: ["عالي الألياف", "قليل السعرات", "مضادات أكسدة"],
        tagClasses: ["tag-fiber", "tag-keto", "tag-vegan"],
        icons: ["🥗", "❤️"],
        note: "غني بالألياف ومضادات الأكسدة",
        goals: ["weight_loss", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 17,
        name: "تمر",
        nameEn: "Dates",
        category: "carbs",
        calories: 277,
        protein: 1.8,
        carbs: 75,
        fat: 0.2,
        image: "🫒",
        tags: ["طاقة سريعة", "طبيعي", "غني بالمعادن"],
        tagClasses: ["tag-vegan", "tag-vegan", "tag-vegan"],
        icons: ["⚡", "🌟"],
        note: "مصدر طبيعي للسكريات والطاقة السريعة",
        goals: ["muscle_gain"],
        calorieLevel: "high"
    },

    // HEALTHY FATS
    {
        id: 18,
        name: "لوز",
        nameEn: "Almonds",
        category: "fats",
        calories: 579,
        protein: 21,
        carbs: 22,
        fat: 50,
        image: "🌰",
        tags: ["دهون صحية", "عالي البروتين", "فيتامين E"],
        tagClasses: ["tag-vegan", "tag-protein", "tag-vegan"],
        icons: ["❤️", "🧠"],
        note: "غني بالدهون الأحادية غير المشبعة وفيتامين E",
        goals: ["muscle_gain", "maintenance"],
        calorieLevel: "high"
    },
    {
        id: 19,
        name: "جوز",
        nameEn: "Walnuts",
        category: "fats",
        calories: 654,
        protein: 15,
        carbs: 14,
        fat: 65,
        image: "🥜",
        tags: ["أوميغا 3", "صحي للدماغ", "مضادات أكسدة"],
        tagClasses: ["tag-vegan", "tag-vegan", "tag-vegan"],
        icons: ["🧠", "❤️"],
        note: "أفضل مصدر نباتي لأحماض أوميغا 3",
        goals: ["maintenance"],
        calorieLevel: "high"
    },
    {
        id: 20,
        name: "فول سوداني",
        nameEn: "Peanuts",
        category: "fats",
        calories: 567,
        protein: 26,
        carbs: 16,
        fat: 49,
        image: "🥜",
        tags: ["عالي البروتين", "اقتصادي", "دهون صحية"],
        tagClasses: ["tag-protein", "tag-budget", "tag-vegan"],
        icons: ["💪", "💰"],
        note: "مصدر اقتصادي للبروتين والدهون الصحية",
        goals: ["muscle_gain", "maintenance"],
        calorieLevel: "high"
    },
    {
        id: 21,
        name: "زيت الزيتون",
        nameEn: "Olive Oil",
        category: "fats",
        calories: 884,
        protein: 0,
        carbs: 0,
        fat: 100,
        image: "🫒",
        tags: ["دهون أحادية", "مضادات أكسدة", "صحي للقلب"],
        tagClasses: ["tag-vegan", "tag-vegan", "tag-vegan"],
        icons: ["❤️", "🌿"],
        note: "أفضل زيت للطبخ والسلطات، غني بمضادات الأكسدة",
        goals: ["maintenance"],
        calorieLevel: "high"
    },
    {
        id: 22,
        name: "زيت جوز الهند",
        nameEn: "Coconut Oil",
        category: "fats",
        calories: 862,
        protein: 0,
        carbs: 0,
        fat: 100,
        image: "🥥",
        tags: ["MCT", "صديق الكيتو", "طبيعي"],
        tagClasses: ["tag-keto", "tag-keto", "tag-vegan"],
        icons: ["🔥", "🥥"],
        note: "يحتوي على أحماض دهنية متوسطة السلسلة سريعة الحرق",
        goals: ["weight_loss", "maintenance"],
        calorieLevel: "high"
    },
    {
        id: 23,
        name: "أفوكادو",
        nameEn: "Avocado",
        category: "fats",
        calories: 160,
        protein: 2,
        carbs: 9,
        fat: 15,
        image: "🥑",
        tags: ["دهون أحادية", "عالي الألياف", "بوتاسيوم"],
        tagClasses: ["tag-vegan", "tag-fiber", "tag-vegan"],
        icons: ["❤️", "🌱"],
        note: "غني بالدهون الصحية والألياف والبوتاسيوم",
        goals: ["maintenance"],
        calorieLevel: "medium"
    },
    {
        id: 24,
        name: "زبدة الفول السوداني",
        nameEn: "Peanut Butter",
        category: "fats",
        calories: 588,
        protein: 25,
        carbs: 20,
        fat: 50,
        image: "🥜",
        tags: ["عالي البروتين", "طاقة مكثفة", "اقتصادي"],
        tagClasses: ["tag-protein", "tag-vegan", "tag-budget"],
        icons: ["💪", "⚡"],
        note: "مصدر مكثف للطاقة والبروتين، مثالي لزيادة الوزن",
        goals: ["muscle_gain"],
        calorieLevel: "high"
    },

    // FRUITS & VEGETABLES
    {
        id: 25,
        name: "سبانخ",
        nameEn: "Spinach",
        category: "fruits",
        calories: 23,
        protein: 2.9,
        carbs: 3.6,
        fat: 0.4,
        image: "🥬",
        tags: ["عالي الحديد", "قليل السعرات", "مضادات أكسدة"],
        tagClasses: ["tag-vegan", "tag-keto", "tag-vegan"],
        icons: ["🥗", "💪"],
        note: "غني بالحديد وحمض الفوليك ومضادات الأكسدة",
        goals: ["weight_loss", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 26,
        name: "بروكلي",
        nameEn: "Broccoli",
        category: "fruits",
        calories: 34,
        protein: 2.8,
        carbs: 7,
        fat: 0.4,
        image: "🥦",
        tags: ["عالي الألياف", "فيتامين C", "مضادات أكسدة"],
        tagClasses: ["tag-fiber", "tag-vegan", "tag-vegan"],
        icons: ["🥗", "🛡️"],
        note: "سوبرفود غني بالفيتامينات ومضادات الأكسدة",
        goals: ["weight_loss", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 27,
        name: "جزر",
        nameEn: "Carrots",
        category: "fruits",
        calories: 41,
        protein: 0.9,
        carbs: 10,
        fat: 0.2,
        image: "🥕",
        tags: ["بيتا كاروتين", "قليل السعرات", "صحي للعيون"],
        tagClasses: ["tag-vegan", "tag-keto", "tag-vegan"],
        icons: ["👁️", "🥗"],
        note: "غني بالبيتا كاروتين المفيد لصحة العيون",
        goals: ["weight_loss", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 28,
        name: "فلفل ملون",
        nameEn: "Bell Peppers",
        category: "fruits",
        calories: 31,
        protein: 1,
        carbs: 7,
        fat: 0.3,
        image: "🫑",
        tags: ["فيتامين C", "قليل السعرات", "ملون"],
        tagClasses: ["tag-vegan", "tag-keto", "tag-vegan"],
        icons: ["🥗", "🌈"],
        note: "يحتوي على فيتامين C أكثر من البرتقال",
        goals: ["weight_loss", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 29,
        name: "فراولة",
        nameEn: "Strawberries",
        category: "fruits",
        calories: 32,
        protein: 0.7,
        carbs: 8,
        fat: 0.3,
        image: "🍓",
        tags: ["مضادات أكسدة", "قليل السعرات", "فيتامين C"],
        tagClasses: ["tag-vegan", "tag-keto", "tag-vegan"],
        icons: ["❤️", "🥗"],
        note: "غني بمضادات الأكسدة وفيتامين C",
        goals: ["weight_loss", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 30,
        name: "توت أزرق",
        nameEn: "Blueberries",
        category: "fruits",
        calories: 57,
        protein: 0.7,
        carbs: 14,
        fat: 0.3,
        image: "🫐",
        tags: ["سوبرفود", "مضادات أكسدة", "صحي للدماغ"],
        tagClasses: ["tag-vegan", "tag-vegan", "tag-vegan"],
        icons: ["🧠", "⭐"],
        note: "أعلى مصدر لمضادات الأكسدة في الفواكه",
        goals: ["weight_loss", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 31,
        name: "خيار",
        nameEn: "Cucumber",
        category: "fruits",
        calories: 16,
        protein: 0.7,
        carbs: 4,
        fat: 0.1,
        image: "🥒",
        tags: ["قليل السعرات", "مرطب", "منعش"],
        tagClasses: ["tag-keto", "tag-vegan", "tag-vegan"],
        icons: ["🥗", "💧"],
        note: "95% ماء، مثالي للترطيب وفقدان الوزن",
        goals: ["weight_loss"],
        calorieLevel: "low"
    },
    {
        id: 32,
        name: "طماطم",
        nameEn: "Tomatoes",
        category: "fruits",
        calories: 18,
        protein: 0.9,
        carbs: 3.9,
        fat: 0.2,
        image: "🍅",
        tags: ["ليكوبين", "قليل السعرات", "مضادات أكسدة"],
        tagClasses: ["tag-vegan", "tag-keto", "tag-vegan"],
        icons: ["❤️", "🥗"],
        note: "غني بالليكوبين المضاد للأكسدة",
        goals: ["weight_loss", "maintenance"],
        calorieLevel: "low"
    },

    // SUPPLEMENTS
    {
        id: 33,
        name: "بروتين مصل اللبن",
        nameEn: "Whey Protein",
        category: "supplements",
        calories: 103,
        protein: 20,
        carbs: 2,
        fat: 1,
        image: "🥤",
        tags: ["بروتين سريع", "بناء العضلات", "بعد التمرين"],
        tagClasses: ["tag-protein", "tag-protein", "tag-protein"],
        icons: ["💪", "⚡"],
        note: "أسرع بروتين امتصاصاً، مثالي بعد التمرين",
        goals: ["muscle_gain"],
        calorieLevel: "low"
    },
    {
        id: 34,
        name: "كرياتين",
        nameEn: "Creatine",
        category: "supplements",
        calories: 0,
        protein: 0,
        carbs: 0,
        fat: 0,
        image: "💊",
        tags: ["قوة", "أداء", "مثبت علمياً"],
        tagClasses: ["tag-protein", "tag-protein", "tag-protein"],
        icons: ["💪", "🔬"],
        note: "يزيد القوة والأداء في التمارين عالية الكثافة",
        goals: ["muscle_gain"],
        calorieLevel: "low"
    },
    {
        id: 35,
        name: "أحماض أمينية متفرعة",
        nameEn: "BCAA",
        category: "supplements",
        calories: 4,
        protein: 1,
        carbs: 0,
        fat: 0,
        image: "🧪",
        tags: ["استشفاء", "أثناء التمرين", "مضاد للهدم"],
        tagClasses: ["tag-protein", "tag-protein", "tag-protein"],
        icons: ["🔄", "💪"],
        note: "يساعد في الاستشفاء ومنع هدم العضلات",
        goals: ["muscle_gain"],
        calorieLevel: "low"
    },
    {
        id: 36,
        name: "فيتامينات متعددة",
        nameEn: "Multivitamins",
        category: "supplements",
        calories: 5,
        protein: 0,
        carbs: 1,
        fat: 0,
        image: "💊",
        tags: ["صحة عامة", "فيتامينات", "معادن"],
        tagClasses: ["tag-vegan", "tag-vegan", "tag-vegan"],
        icons: ["🛡️", "⭐"],
        note: "يغطي النقص في الفيتامينات والمعادن اليومية",
        goals: ["maintenance"],
        calorieLevel: "low"
    },

    // Additional Foods to reach 50+
    {
        id: 37,
        name: "زبادي يوناني",
        nameEn: "Greek Yogurt",
        category: "protein",
        calories: 59,
        protein: 10,
        carbs: 3.6,
        fat: 0.4,
        image: "🥛",
        tags: ["بروبيوتيك", "عالي البروتين", "قليل الدهون"],
        tagClasses: ["tag-protein", "tag-protein", "tag-keto"],
        icons: ["🥗", "🦠"],
        note: "غني بالبروتين والبروبيوتيك المفيد للهضم",
        goals: ["weight_loss", "muscle_gain"],
        calorieLevel: "low"
    },
    {
        id: 38,
        name: "بطاطا حلوة",
        nameEn: "Sweet Potato",
        category: "carbs",
        calories: 86,
        protein: 1.6,
        carbs: 20,
        fat: 0.1,
        image: "🍠",
        tags: ["بيتا كاروتين", "كربوهيدرات معقدة", "عالي الألياف"],
        tagClasses: ["tag-vegan", "tag-fiber", "tag-vegan"],
        icons: ["⚡", "👁️"],
        note: "مصدر ممتاز للكربوهيدرات المعقدة والبيتا كاروتين",
        goals: ["muscle_gain", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 39,
        name: "كيوي",
        nameEn: "Kiwi",
        category: "fruits",
        calories: 61,
        protein: 1.1,
        carbs: 15,
        fat: 0.5,
        image: "🥝",
        tags: ["فيتامين C", "عالي الألياف", "هضم"],
        tagClasses: ["tag-vegan", "tag-fiber", "tag-vegan"],
        icons: ["🥗", "💚"],
        note: "يحتوي على فيتامين C أكثر من البرتقال وإنزيمات هاضمة",
        goals: ["weight_loss", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 40,
        name: "بذور الشيا",
        nameEn: "Chia Seeds",
        category: "fats",
        calories: 486,
        protein: 17,
        carbs: 42,
        fat: 31,
        image: "🌱",
        tags: ["أوميغا 3", "عالي الألياف", "سوبرفود"],
        tagClasses: ["tag-vegan", "tag-fiber", "tag-vegan"],
        icons: ["🧠", "⭐"],
        note: "غني بأوميغا 3 والألياف والبروتين النباتي",
        goals: ["maintenance"],
        calorieLevel: "high"
    },
    {
        id: 41,
        name: "كركم",
        nameEn: "Turmeric",
        category: "supplements",
        calories: 354,
        protein: 8,
        carbs: 65,
        fat: 10,
        image: "🟡",
        tags: ["مضاد التهاب", "مضادات أكسدة", "طبيعي"],
        tagClasses: ["tag-vegan", "tag-vegan", "tag-vegan"],
        icons: ["🛡️", "🌿"],
        note: "مضاد طبيعي للالتهابات ومضاد للأكسدة",
        goals: ["maintenance"],
        calorieLevel: "high"
    },
    {
        id: 42,
        name: "زنجبيل",
        nameEn: "Ginger",
        category: "supplements",
        calories: 80,
        protein: 1.8,
        carbs: 18,
        fat: 0.8,
        image: "🫚",
        tags: ["مضاد غثيان", "هضم", "طبيعي"],
        tagClasses: ["tag-vegan", "tag-vegan", "tag-vegan"],
        icons: ["🌿", "💚"],
        note: "مفيد للهضم ومضاد للغثيان والالتهابات",
        goals: ["maintenance"],
        calorieLevel: "low"
    },
    {
        id: 43,
        name: "أناناس",
        nameEn: "Pineapple",
        category: "fruits",
        calories: 50,
        protein: 0.5,
        carbs: 13,
        fat: 0.1,
        image: "🍍",
        tags: ["إنزيمات هاضمة", "فيتامين C", "مضاد التهاب"],
        tagClasses: ["tag-vegan", "tag-vegan", "tag-vegan"],
        icons: ["💚", "🌟"],
        note: "يحتوي على إنزيم البروميلين المفيد للهضم",
        goals: ["weight_loss", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 44,
        name: "مانجو",
        nameEn: "Mango",
        category: "fruits",
        calories: 60,
        protein: 0.8,
        carbs: 15,
        fat: 0.4,
        image: "🥭",
        tags: ["فيتامين A", "مضادات أكسدة", "طبيعي"],
        tagClasses: ["tag-vegan", "tag-vegan", "tag-vegan"],
        icons: ["👁️", "🌟"],
        note: "غني بفيتامين A ومضادات الأكسدة",
        goals: ["maintenance"],
        calorieLevel: "low"
    },
    {
        id: 45,
        name: "بذور عباد الشمس",
        nameEn: "Sunflower Seeds",
        category: "fats",
        calories: 584,
        protein: 21,
        carbs: 20,
        fat: 51,
        image: "🌻",
        tags: ["فيتامين E", "عالي البروتين", "اقتصادي"],
        tagClasses: ["tag-protein", "tag-vegan", "tag-budget"],
        icons: ["💪", "💰"],
        note: "مصدر ممتاز لفيتامين E والدهون الصحية",
        goals: ["muscle_gain", "maintenance"],
        calorieLevel: "high"
    },
    {
        id: 46,
        name: "كاجو",
        nameEn: "Cashews",
        category: "fats",
        calories: 553,
        protein: 18,
        carbs: 30,
        fat: 44,
        image: "🥜",
        tags: ["دهون صحية", "مغنيسيوم", "كريمي"],
        tagClasses: ["tag-vegan", "tag-vegan", "tag-vegan"],
        icons: ["❤️", "🧠"],
        note: "غني بالمغنيسيوم والدهون الأحادية غير المشبعة",
        goals: ["maintenance"],
        calorieLevel: "high"
    },
    {
        id: 47,
        name: "بازلاء خضراء",
        nameEn: "Green Peas",
        category: "protein",
        calories: 81,
        protein: 5.4,
        carbs: 14,
        fat: 0.4,
        image: "🟢",
        tags: ["نباتي", "عالي الألياف", "بروتين"],
        tagClasses: ["tag-vegan", "tag-fiber", "tag-protein"],
        icons: ["🌱", "💚"],
        note: "مصدر نباتي جيد للبروتين والألياف",
        goals: ["weight_loss", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 48,
        name: "فاصوليا سوداء",
        nameEn: "Black Beans",
        category: "protein",
        calories: 132,
        protein: 8.9,
        carbs: 23,
        fat: 0.5,
        image: "⚫",
        tags: ["نباتي", "عالي الألياف", "اقتصادي"],
        tagClasses: ["tag-vegan", "tag-fiber", "tag-budget"],
        icons: ["🌱", "💰"],
        note: "غني بالبروتين النباتي والألياف والحديد",
        goals: ["weight_loss", "maintenance"],
        calorieLevel: "low"
    },
    {
        id: 49,
        name: "بذور اليقطين",
        nameEn: "Pumpkin Seeds",
        category: "fats",
        calories: 559,
        protein: 19,
        carbs: 54,
        fat: 49,
        image: "🎃",
        tags: ["زنك", "مغنيسيوم", "دهون صحية"],
        tagClasses: ["tag-vegan", "tag-vegan", "tag-vegan"],
        icons: ["💪", "🧠"],
        note: "غني بالزنك والمغنيسيوم والدهون الصحية",
        goals: ["muscle_gain", "maintenance"],
        calorieLevel: "high"
    },
    {
        id: 50,
        name: "رمان",
        nameEn: "Pomegranate",
        category: "fruits",
        calories: 83,
        protein: 1.7,
        carbs: 19,
        fat: 1.2,
        image: "🍇",
        tags: ["مضادات أكسدة", "صحي للقلب", "مضاد التهاب"],
        tagClasses: ["tag-vegan", "tag-vegan", "tag-vegan"],
        icons: ["❤️", "🛡️"],
        note: "أعلى مصدر لمضادات الأكسدة، مفيد لصحة القلب",
        goals: ["maintenance"],
        calorieLevel: "low"
    }
];

// Tips of the day
const tipsOfDay = [
    "هل تعلم أن البروتين يحرق سعرات حرارية أكثر أثناء الهضم من الكربوهيدرات والدهون؟",
    "تناول الفواكه والخضار الملونة يضمن حصولك على مجموعة متنوعة من الفيتامينات!",
    "شرب الماء قبل الوجبات يساعد في الشعور بالشبع وتقليل السعرات المتناولة",
    "الدهون الصحية مثل الأفوكادو واللوز ضرورية لامتصاص الفيتامينات الذائبة في الدهون",
    "تناول البروتين خلال 30 دقيقة بعد التمرين يساعد في بناء العضلات بشكل أفضل",
    "الألياف تساعد في الشعور بالشبع لفترة أطول وتحسن صحة الجهاز الهضمي",
    "تقسيم الوجبات إلى 5-6 وجبات صغيرة يساعد في تسريع عملية الأيض"
];

// Global variables
let currentFilters = {
    category: 'all',
    goal: null,
    calories: null,
    search: ''
};

let viewedFoods = new Set();
let currentTipIndex = 0;

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Starting initialization');
    
    // Check if required elements exist
    const requiredElements = [
        'foodsContainer',
        'searchInput'
    ];
    
    const missingElements = requiredElements.filter(id => !document.getElementById(id));
    
    if (missingElements.length > 0) {
        console.error('Missing required elements:', missingElements);
        return;
    }
    
    // Check for filter elements (they use classes, not IDs)
    const filterTabs = document.querySelectorAll('.filter-tab');
    const secondaryFilters = document.querySelectorAll('.secondary-filter');
    
    if (filterTabs.length === 0) {
        console.error('No filter tabs found');
        return;
    }
    
    if (secondaryFilters.length === 0) {
        console.error('No secondary filters found');
        return;
    }
    
    console.log('All required elements found');
    console.log('Food database length:', foodDatabase.length);
    console.log('Filter tabs found:', filterTabs.length);
    console.log('Secondary filters found:', secondaryFilters.length);
    
    try {
        initializePage();
        setupEventListeners();
        
        // Show loading animation first
        showLoading();
        
        // Display foods after a short delay to ensure DOM is ready
        setTimeout(() => {
            console.log('Displaying foods after delay');
            hideLoading();
            displayFoods(foodDatabase);
            console.log('Foods displayed');
        }, 500);
        
        rotateTipOfDay();
        
        console.log('Initialization completed successfully');
    } catch (error) {
        console.error('Error during initialization:', error);
        hideLoading();
    }
});

function showLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.classList.add('show');
    }
}

function hideLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.classList.remove('show');
    }
}

function initializePage() {
    console.log('Initializing page...');
    
    // Set random tip of the day
    const randomTip = tipsOfDay[Math.floor(Math.random() * tipsOfDay.length)];
    const tipElement = document.getElementById('tipOfDay');
    if (tipElement) {
        tipElement.textContent = randomTip;
    }
    
    // Initialize progress tracker
    updateProgress();
}

function setupEventListeners() {
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', handleSearch);
    
    // Category filters
    const categoryTabs = document.querySelectorAll('.filter-tab');
    categoryTabs.forEach(tab => {
        tab.addEventListener('click', () => handleCategoryFilter(tab));
    });
    
    // Secondary filters
    const secondaryFilters = document.querySelectorAll('.secondary-filter');
    secondaryFilters.forEach(filter => {
        filter.addEventListener('click', () => handleSecondaryFilter(filter));
    });
}

function handleSearch(event) {
    currentFilters.search = event.target.value.toLowerCase();
    filterAndDisplayFoods();
}

function handleCategoryFilter(tab) {
    // Remove active class from all tabs
    document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
    
    // Add active class to clicked tab
    tab.classList.add('active');
    
    // Update filter
    currentFilters.category = tab.dataset.category;
    
    // Filter and display foods
    filterAndDisplayFoods();
}

function handleSecondaryFilter(filter) {
    // Toggle active state
    filter.classList.toggle('active');
    
    // Update filters based on data attributes
    if (filter.dataset.goal) {
        currentFilters.goal = filter.classList.contains('active') ? filter.dataset.goal : null;
        
        // Remove other goal filters
        document.querySelectorAll('.secondary-filter[data-goal]').forEach(f => {
            if (f !== filter) f.classList.remove('active');
        });
    }
    
    if (filter.dataset.calories) {
        currentFilters.calories = filter.classList.contains('active') ? filter.dataset.calories : null;
        
        // Remove other calorie filters
        document.querySelectorAll('.secondary-filter[data-calories]').forEach(f => {
            if (f !== filter) f.classList.remove('active');
        });
    }
    
    filterAndDisplayFoods();
}

function filterAndDisplayFoods() {
    let filteredFoods = foodDatabase.filter(food => {
        // Category filter
        if (currentFilters.category !== 'all' && food.category !== currentFilters.category) {
            return false;
        }
        
        // Search filter
        if (currentFilters.search && 
            !food.name.toLowerCase().includes(currentFilters.search) &&
            !food.nameEn.toLowerCase().includes(currentFilters.search)) {
            return false;
        }
        
        // Goal filter
        if (currentFilters.goal && !food.goals.includes(currentFilters.goal)) {
            return false;
        }
        
        // Calorie filter
        if (currentFilters.calories && food.calorieLevel !== currentFilters.calories) {
            return false;
        }
        
        return true;
    });
    
    displayFoods(filteredFoods);
}

function displayFoods(foods) {
    console.log('Displaying foods:', foods.length);
    
    const container = document.getElementById('foodsContainer');
    const noResults = document.getElementById('noResults');
    
    if (!container) {
        console.error('Foods container not found!');
        return;
    }
    
    if (foods.length === 0) {
        container.innerHTML = '';
        if (noResults) {
            noResults.style.display = 'block';
        }
        return;
    }
    
    if (noResults) {
        noResults.style.display = 'none';
    }
    
    // Group foods by category
    const groupedFoods = groupFoodsByCategory(foods);
    console.log('Grouped foods:', groupedFoods);
    
    let html = '';
    
    Object.keys(groupedFoods).forEach(category => {
        if (groupedFoods[category].length > 0) {
            console.log(`Adding ${category} section with ${groupedFoods[category].length} foods`);
            html += createCategorySection(category, groupedFoods[category]);
        }
    });
    
    if (html === '') {
        console.warn('No HTML generated for foods');
        container.innerHTML = '<div style="text-align: center; padding: 2rem;"><h3>لا توجد أطعمة للعرض</h3></div>';
        return;
    }
    
    container.innerHTML = html;
    console.log('HTML set to container');
    
    // Add fade-in animation
    setTimeout(() => {
        const foodCards = document.querySelectorAll('.food-card');
        console.log('Found food cards:', foodCards.length);
        
        foodCards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in');
            }, index * 50);
        });
    }, 100);
    
    // Add click listeners for progress tracking
    document.querySelectorAll('.food-card').forEach(card => {
        card.addEventListener('click', () => {
            const foodId = parseInt(card.dataset.foodId);
            viewedFoods.add(foodId);
            updateProgress();
        });
    });
}

function groupFoodsByCategory(foods) {
    const categories = {
        protein: [],
        carbs: [],
        fats: [],
        fruits: [],
        supplements: []
    };
    
    foods.forEach(food => {
        if (categories[food.category]) {
            categories[food.category].push(food);
        }
    });
    
    return categories;
}

function createCategorySection(category, foods) {
    if (!category || !foods || foods.length === 0) {
        console.warn('Invalid category or foods data:', category, foods);
        return '';
    }
    
    console.log(`Creating section for category: ${category} with ${foods.length} foods`);
    
    const categoryInfo = getCategoryInfo(category);
    
    const foodCardsHtml = foods.map(food => createFoodCard(food)).filter(card => card !== '').join('');
    
    if (foodCardsHtml === '') {
        console.warn(`No valid food cards generated for category: ${category}`);
        return '';
    }
    
    return `
        <div class="category-section" data-category="${category}">
            <div class="category-header">
                <div class="category-icon">${categoryInfo.icon}</div>
                <div class="category-info">
                    <h2>${categoryInfo.title}</h2>
                    <p>${categoryInfo.description}</p>
                </div>
                <div class="category-count">${foods.length} عنصر</div>
            </div>
            <div class="foods-grid">
                ${foodCardsHtml}
            </div>
        </div>
    `;
}

function getCategoryInfo(category) {
    const categoryMap = {
        protein: {
            title: 'البروتينات',
            icon: '🥩',
            color: 'var(--protein-color)',
            description: 'مصادر البروتين عالي الجودة لبناء العضلات والاستشفاء'
        },
        carbs: {
            title: 'الكربوهيدرات',
            icon: '🍞',
            color: 'var(--carbs-color)',
            description: 'مصادر الطاقة الأساسية للجسم والدماغ'
        },
        fats: {
            title: 'الدهون الصحية',
            icon: '🥑',
            color: 'var(--fats-color)',
            description: 'الدهون الضرورية لصحة القلب وامتصاص الفيتامينات'
        },
        fruits: {
            title: 'الفواكه والخضار',
            icon: '🍎',
            color: 'var(--fruits-color)',
            description: 'مصادر الفيتامينات والمعادن ومضادات الأكسدة'
        },
        supplements: {
            title: 'المكملات الغذائية',
            icon: '💊',
            color: 'var(--supplements-color)',
            description: 'مكملات لتحسين الأداء والصحة العامة'
        }
    };
    
    return categoryMap[category] || categoryMap.protein;
}

function createFoodCard(food) {
    if (!food) {
        console.error('Food data is null or undefined');
        return '';
    }
    
    console.log('Creating card for:', food.name);
    
    const tagsHtml = food.tags && food.tagClasses ? 
        food.tags.map((tag, index) => 
            `<span class="food-tag ${food.tagClasses[index] || 'tag-protein'}">${tag}</span>`
        ).join('') : '';
    
    const iconsHtml = food.icons ? 
        food.icons.map(icon => 
            `<span class="diet-icon">${icon}</span>`
        ).join('') : '';
    
    return `
        <div class="food-card ${food.category || 'protein'}" data-food-id="${food.id || 0}">
            <div class="food-header">
                <div class="food-image">${food.image || '🍽️'}</div>
                <div class="food-info">
                    <h3>${food.name || 'غير محدد'}</h3>
                    <div class="food-calories">${food.calories || 0} سعرة/100جم</div>
                </div>
            </div>
            
            <div class="macros-row">
                <div class="macro-item">
                    <div class="macro-value">${food.protein || 0}جم</div>
                    <div class="macro-label">بروتين</div>
                </div>
                <div class="macro-item">
                    <div class="macro-value">${food.carbs || 0}جم</div>
                    <div class="macro-label">كربوهيدرات</div>
                </div>
                <div class="macro-item">
                    <div class="macro-value">${food.fat || 0}جم</div>
                    <div class="macro-label">دهون</div>
                </div>
            </div>
            
            <div class="food-tags">
                ${tagsHtml}
            </div>
            
            <div class="food-icons">
                ${iconsHtml}
            </div>
            
            <div class="food-note">
                ${food.note || 'لا توجد ملاحظات إضافية'}
            </div>
        </div>
    `;
}

function updateProgress() {
    const totalFoods = foodDatabase.length;
    const viewedCount = viewedFoods.size;
    const percentage = (viewedCount / totalFoods) * 100;
    
    document.getElementById('progressFill').style.width = `${percentage}%`;
    document.getElementById('progressText').textContent = `${viewedCount} من ${totalFoods}+ طعام`;
}

function rotateTipOfDay() {
    setInterval(() => {
        currentTipIndex = (currentTipIndex + 1) % tipsOfDay.length;
        document.getElementById('tipOfDay').textContent = tipsOfDay[currentTipIndex];
    }, 10000); // Change tip every 10 seconds
}

// Sorting functionality
function sortFoods(criteria) {
    let sortedFoods = [...foodDatabase];
    
    switch(criteria) {
        case 'protein':
            sortedFoods.sort((a, b) => b.protein - a.protein);
            break;
        case 'calories':
            sortedFoods.sort((a, b) => a.calories - b.calories);
            break;
        case 'popular':
            // Sort by viewed count (mock popularity)
            sortedFoods.sort((a, b) => {
                const aViewed = viewedFoods.has(a.id) ? 1 : 0;
                const bViewed = viewedFoods.has(b.id) ? 1 : 0;
                return bViewed - aViewed;
            });
            break;
        default:
            // Default alphabetical sort
            sortedFoods.sort((a, b) => a.name.localeCompare(b.name, 'ar'));
    }
    
    displayFoods(sortedFoods);
}

// Export functions for potential future use
window.foodGuide = {
    sortFoods,
    filterAndDisplayFoods,
    foodDatabase
};