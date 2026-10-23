export interface SdgMeta {
  goal: number;
  name: string;
  color: string;
  shortDesc: string;
  icon: string;
}

export const SDG_METADATA: Record<number, SdgMeta> = {
  1: { goal: 1, name: "No Poverty", color: "#E5243B", shortDesc: "End poverty in all its forms everywhere.", icon: "Target" },
  2: { goal: 2, name: "Zero Hunger", color: "#DDA63A", shortDesc: "End hunger, achieve food security and improved nutrition.", icon: "Utensils" },
  3: { goal: 3, name: "Good Health and Well-being", color: "#4C9F38", shortDesc: "Ensure healthy lives and promote well-being for all at all ages.", icon: "HeartPulse" },
  4: { goal: 4, name: "Quality Education", color: "#C5192D", shortDesc: "Ensure inclusive and equitable quality education and lifelong learning.", icon: "GraduationCap" },
  5: { goal: 5, name: "Gender Equality", color: "#FF3A21", shortDesc: "Achieve gender equality and empower all women and girls.", icon: "Users" },
  6: { goal: 6, name: "Clean Water and Sanitation", color: "#26BDE2", shortDesc: "Ensure availability and sustainable management of water and sanitation.", icon: "Droplets" },
  7: { goal: 7, name: "Affordable and Clean Energy", color: "#FCC30B", shortDesc: "Ensure access to affordable, reliable, sustainable modern energy.", icon: "Zap" },
  8: { goal: 8, name: "Decent Work and Economic Growth", color: "#A21942", shortDesc: "Promote sustained, inclusive and sustainable economic growth, full and productive employment.", icon: "Briefcase" },
  9: { goal: 9, name: "Industry, Innovation and Infrastructure", color: "#FD6925", shortDesc: "Build resilient infrastructure, promote inclusive and sustainable industrialization.", icon: "Cpu" },
  10: { goal: 10, name: "Reduced Inequalities", color: "#DD1367", shortDesc: "Reduce inequality within and among countries.", icon: "Scale" },
  11: { goal: 11, name: "Sustainable Cities and Communities", color: "#FD9D24", shortDesc: "Make cities and human settlements inclusive, safe, resilient.", icon: "Building2" },
  12: { goal: 12, name: "Responsible Consumption and Production", color: "#BF8B2E", shortDesc: "Ensure sustainable consumption and production patterns.", icon: "Recycle" },
  13: { goal: 13, name: "Climate Action", color: "#3F7E44", shortDesc: "Take urgent action to combat climate change and its impacts.", icon: "Leaf" },
  14: { goal: 14, name: "Life Below Water", color: "#0A97D9", shortDesc: "Conserve and sustainably use the oceans, seas and marine resources.", icon: "Fish" },
  15: { goal: 15, name: "Life on Land", color: "#56C02B", shortDesc: "Protect, restore and promote sustainable use of terrestrial ecosystems.", icon: "Trees" },
  16: { goal: 16, name: "Peace, Justice and Strong Institutions", color: "#00689D", shortDesc: "Promote peaceful and inclusive societies for sustainable development.", icon: "ShieldCheck" },
  17: { goal: 17, name: "Partnerships for the Goals", color: "#19486A", shortDesc: "Strengthen the means of implementation and revitalize partnerships.", icon: "Globe" },
};
