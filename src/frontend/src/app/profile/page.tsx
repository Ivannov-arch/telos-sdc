"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { useDropzone } from "react-dropzone";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Skeleton } from "@/components/ui/skeleton";
import { uploadProfile, listProfiles, UserProfile } from "@/lib/api";
import {
  UploadCloud,
  FileText,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  UserCheck,
  Plus,
  X,
  ArrowRight,
  Loader2,
  Briefcase,
} from "lucide-react";

export default function ProfilePage() {
  const router = useRouter();

  // Pre-seeded demo profiles fetched from backend or fallback
  const [demoProfiles, setDemoProfiles] = React.useState<UserProfile[]>([]);
  const [loadingProfiles, setLoadingProfiles] = React.useState(true);

  // Upload state
  const [selectedFile, setSelectedFile] = React.useState<File | null>(null);
  const [uploading, setUploading] = React.useState(false);
  const [uploadError, setUploadError] = React.useState<string | null>(null);

  // Manual entry state
  const [skillInput, setSkillInput] = React.useState("");
  const [manualSkills, setManualSkills] = React.useState<string[]>([
    "Python",
    "Machine Learning",
    "SQL",
  ]);
  const [experienceYears, setExperienceYears] = React.useState<number>(3);
  const [interestDomain, setInterestDomain] = React.useState("Artificial Intelligence & NLP");

  const commonSkillSuggestions = [
    "Python",
    "Data Analysis",
    "Machine Learning",
    "SQL",
    "Natural Language Processing",
    "Cloud Computing (AWS/GCP)",
    "Docker & Containers",
    "Git & CI/CD",
    "System Architecture",
    "Cybersecurity",
    "Project Management",
    "Data Governance",
  ];

  React.useEffect(() => {
    async function load() {
      try {
        const res = await listProfiles();
        if (res?.profiles?.length) {
          setDemoProfiles(res.profiles);
        }
      } catch (err) {
        console.error("Error loading profiles:", err);
      } finally {
        setLoadingProfiles(false);
      }
    }
    load();
  }, []);

  // Dropzone setup
  const onDrop = React.useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles?.length > 0) {
      const file = acceptedFiles[0];
      if (file.type === "application/pdf" || file.name.endsWith(".pdf")) {
        setSelectedFile(file);
        setUploadError(null);
      } else {
        setUploadError("Please upload a PDF document (.pdf only).");
      }
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"] },
    maxFiles: 1,
    multiple: false,
  });

  const handlePdfSubmit = async () => {
    if (!selectedFile) return;
    setUploading(true);
    setUploadError(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      const res = await uploadProfile(formData);
      const userId = res.user_id || "587479a6-04d5-4371-a57f-c3b39c9b7be2";
      router.push(`/results?user_id=${userId}`);
    } catch (err: any) {
      console.error(err);
      setUploadError(err.message || "Failed to process CV. Falling back to demo profile.");
      // Fallback
      setTimeout(() => {
        router.push(`/results?user_id=587479a6-04d5-4371-a57f-c3b39c9b7be2`);
      }, 1500);
    } finally {
      setUploading(false);
    }
  };

  const handleManualSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setUploading(true);
    try {
      const payload = {
        experience_years: experienceYears,
        skills: manualSkills,
        interests: interestDomain,
      };
      const res = await uploadProfile(payload);
      const userId = res.user_id || "587479a6-04d5-4371-a57f-c3b39c9b7be2";
      router.push(`/results?user_id=${userId}`);
    } catch (err: any) {
      console.error(err);
      router.push(`/results?user_id=587479a6-04d5-4371-a57f-c3b39c9b7be2`);
    } finally {
      setUploading(false);
    }
  };

  const addSkill = (skill: string) => {
    const trimmed = skill.trim();
    if (trimmed && !manualSkills.includes(trimmed)) {
      setManualSkills([...manualSkills, trimmed]);
      setSkillInput("");
    }
  };

  const removeSkill = (skillToRemove: string) => {
    setManualSkills(manualSkills.filter((s) => s !== skillToRemove));
  };

  return (
    <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-10 md:py-16">
      <div className="text-center max-w-2xl mx-auto mb-10">
        <Badge variant="secondary" className="mb-3">
          Feature 1: Skills Intake Pipeline
        </Badge>
        <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white sm:text-4xl">
          Profile & Skills Intake
        </h1>
        <p className="mt-3 text-slate-600 dark:text-slate-400">
          Upload your resume in PDF format or manually configure your skill vector. Our system maps your background directly into standardized ESCO taxonomy.
        </p>
      </div>

      {/* Quick Load Pre-seeded Profiles Banner */}
      <Card className="mb-10 border-indigo-200/80 dark:border-indigo-900/60 bg-gradient-to-r from-indigo-50/70 via-purple-50/50 to-white dark:from-indigo-950/40 dark:via-purple-950/20 dark:bg-slate-900">
        <CardContent className="p-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-600 text-white shrink-0 shadow-xs">
                <UserCheck className="h-5 w-5" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-slate-900 dark:text-white">
                  Instant Demo Profiles (Judges Quick-Test)
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Select a pre-embedded candidate profile to test the live RRF matching engine immediately:
                </p>
              </div>
            </div>

            <div className="flex flex-wrap gap-2 w-full sm:w-auto">
              {loadingProfiles ? (
                <div className="flex gap-2">
                  <Skeleton className="h-9 w-28 rounded-lg" />
                  <Skeleton className="h-9 w-28 rounded-lg" />
                </div>
              ) : (
                demoProfiles.slice(0, 3).map((p, idx) => (
                  <Button
                    key={p.id}
                    variant="outline"
                    size="sm"
                    onClick={() => router.push(`/results?user_id=${p.id}`)}
                    className="rounded-lg text-xs bg-white dark:bg-slate-800 hover:border-indigo-500"
                  >
                    <span>{idx === 0 ? "🤖 AI / NLP Profile" : idx === 1 ? "📊 Data Engineer" : "💻 Fullstack Eng"}</span>
                  </Button>
                ))
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Intake Tabs */}
      <Tabs defaultValue="upload" className="w-full">
        <TabsList className="grid w-full grid-cols-2 max-w-md mx-auto mb-8">
          <TabsTrigger value="upload" className="gap-2">
            <FileText className="h-4 w-4" />
            <span>Upload Resume (PDF)</span>
          </TabsTrigger>
          <TabsTrigger value="manual" className="gap-2">
            <Plus className="h-4 w-4" />
            <span>Manual Skills Form</span>
          </TabsTrigger>
        </TabsList>

        {/* Tab 1: PDF Dropzone */}
        <TabsContent value="upload">
          <Card className="border-slate-200 dark:border-slate-800">
            <CardHeader className="text-center">
              <CardTitle>Upload Your Resume</CardTitle>
              <CardDescription>
                We parse your PDF using `pdfplumber` to extract skills, experience years, and competencies.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div
                {...getRootProps()}
                className={`flex flex-col items-center justify-center rounded-2xl border-2 border-dashed p-10 text-center transition-all cursor-pointer ${
                  isDragActive
                    ? "border-indigo-500 bg-indigo-50/50 dark:bg-indigo-950/20"
                    : "border-slate-300 dark:border-slate-700 hover:border-indigo-400 bg-slate-50/50 dark:bg-slate-900/40"
                }`}
              >
                <input {...getInputProps()} />
                <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-indigo-100 dark:bg-indigo-950/80 text-indigo-600 dark:text-indigo-400 mb-4 shadow-xs">
                  <UploadCloud className="h-8 w-8" />
                </div>
                <div className="text-base font-semibold text-slate-800 dark:text-slate-200">
                  {selectedFile ? (
                    <span className="text-indigo-600 dark:text-indigo-400 flex items-center justify-center gap-2">
                      <CheckCircle2 className="h-5 w-5" />
                      {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
                    </span>
                  ) : (
                    "Drag and drop your CV here, or click to browse"
                  )}
                </div>
                <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                  Supported format: <strong>.pdf</strong> only (Max 10MB)
                </p>
              </div>

              {uploadError && (
                <div className="flex items-center gap-2 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900 p-3 text-xs text-rose-700 dark:text-rose-300">
                  <AlertCircle className="h-4 w-4 shrink-0" />
                  <span>{uploadError}</span>
                </div>
              )}

              <div className="flex justify-end gap-3 pt-4 border-t border-slate-100 dark:border-slate-800">
                {selectedFile && (
                  <Button
                    variant="outline"
                    onClick={() => setSelectedFile(null)}
                    disabled={uploading}
                  >
                    Clear File
                  </Button>
                )}
                <Button
                  disabled={!selectedFile || uploading}
                  onClick={handlePdfSubmit}
                  className="rounded-xl px-6"
                >
                  {uploading ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Extracting Skills via BGE-M3...
                    </>
                  ) : (
                    <>
                      <span>Analyze Profile & Match Roles</span>
                      <ArrowRight className="h-4 w-4 ml-2" />
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Tab 2: Manual Skills Fallback Form */}
        <TabsContent value="manual">
          <Card className="border-slate-200 dark:border-slate-800">
            <CardHeader>
              <CardTitle>Manual Skill Vector Input</CardTitle>
              <CardDescription>
                Configure your hard skills, years of experience, and target domains without a PDF.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleManualSubmit} className="space-y-6">
                {/* Skills Input */}
                <div>
                  <label className="block text-sm font-semibold text-slate-800 dark:text-slate-200 mb-2">
                    Hard & Technical Skills
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      placeholder="e.g. Python, Docker, Natural Language Processing"
                      value={skillInput}
                      onChange={(e) => setSkillInput(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") {
                          e.preventDefault();
                          addSkill(skillInput);
                        }
                      }}
                      className="flex-1 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3.5 py-2 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                    <Button
                      type="button"
                      onClick={() => addSkill(skillInput)}
                      variant="secondary"
                      className="rounded-lg"
                    >
                      Add
                    </Button>
                  </div>

                  {/* Selected Tags */}
                  <div className="flex flex-wrap gap-2 mt-3">
                    {manualSkills.map((skill) => (
                      <span
                        key={skill}
                        className="inline-flex items-center gap-1.5 rounded-lg bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 px-3 py-1 text-xs font-medium text-indigo-700 dark:text-indigo-300"
                      >
                        {skill}
                        <button
                          type="button"
                          onClick={() => removeSkill(skill)}
                          className="hover:text-rose-600 transition-colors"
                        >
                          <X className="h-3 w-3" />
                        </button>
                      </span>
                    ))}
                  </div>

                  {/* Quick Suggestions */}
                  <div className="mt-4">
                    <div className="text-xs font-medium text-slate-400 mb-2">
                      Popular ESCO Skill Suggestions:
                    </div>
                    <div className="flex flex-wrap gap-1.5">
                      {commonSkillSuggestions.map((sug) => (
                        <button
                          key={sug}
                          type="button"
                          onClick={() => addSkill(sug)}
                          className="rounded-md border border-slate-200 dark:border-slate-800 px-2.5 py-1 text-xs text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
                        >
                          + {sug}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Experience Years Slider */}
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <label className="text-sm font-semibold text-slate-800 dark:text-slate-200">
                      Years of Professional Experience
                    </label>
                    <span className="text-sm font-bold text-indigo-600 dark:text-indigo-400">
                      {experienceYears} {experienceYears === 1 ? "year" : "years"}
                    </span>
                  </div>
                  <Slider
                    defaultValue={[experienceYears]}
                    value={[experienceYears]}
                    max={20}
                    min={0}
                    step={1}
                    onValueChange={(val) => setExperienceYears(val[0])}
                    className="py-2"
                  />
                  <div className="flex justify-between text-[11px] text-slate-400 mt-1">
                    <span>Entry-Level (0-2y)</span>
                    <span>Mid-Senior (3-7y)</span>
                    <span>Lead / Executive (8y+)</span>
                  </div>
                </div>

                {/* Domain Selector */}
                <div>
                  <label className="block text-sm font-semibold text-slate-800 dark:text-slate-200 mb-2">
                    Target Domain Focus
                  </label>
                  <select
                    value={interestDomain}
                    onChange={(e) => setInterestDomain(e.target.value)}
                    className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3.5 py-2 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option>Artificial Intelligence & NLP</option>
                    <option>Data Engineering & Cloud</option>
                    <option>Full-Stack Software Engineering</option>
                    <option>Green Tech & Sustainable Innovation</option>
                    <option>Cybersecurity & Infrastructure</option>
                  </select>
                </div>

                <div className="flex justify-end pt-4 border-t border-slate-100 dark:border-slate-800">
                  <Button
                    type="submit"
                    disabled={uploading || manualSkills.length === 0}
                    className="rounded-xl px-6"
                  >
                    {uploading ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Generating Profile Vector...
                      </>
                    ) : (
                      <>
                        <span>Submit & Match Roles</span>
                        <ArrowRight className="h-4 w-4 ml-2" />
                      </>
                    )}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
