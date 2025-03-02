import FileUpload from "./components/fileUpload"
//import DarkModeToggle from "./components/darkMode";
import ColorFilterToggle from "./components/colorFilter";

export function Welcome() {
  return (
    
    <div className="h-screen">
    <main>
      <div className= "p-3 absolute bottom-1 z-10">
        
      <ColorFilterToggle/>
      </div>
      <div className = " w-full bg-white p-6 shadow-lg rounded-lg justify-items-center">
        <h1 className = "text-5xl font-bold text-blue-300">kwikchart</h1>
      </div>
      <div className = "justify-center flex items-center max-h-screen max-w-screen p-20 z-10">
        <FileUpload/>
      </div>
    </main>
    <div className="absolute bottom-0 left-0 w-full overflow-hidden filter-none">
    <svg preserveAspectRatio="none" width='1440' height='200' id="svg" viewBox="0 0 1440 590" xmlns="http://www.w3.org/2000/svg" ><defs><linearGradient id="gradient" x1="0%" y1="50%" x2="100%" y2="50%"><stop offset="5%" stop-color="#7bdcb5"></stop><stop offset="95%" stop-color="#8ED1FC"></stop></linearGradient></defs><path d="M 0,600 L 0,150 C 175.59999999999997,112.93333333333334 351.19999999999993,75.86666666666666 518,97 C 684.8000000000001,118.13333333333334 842.8,197.46666666666667 995,216 C 1147.2,234.53333333333333 1293.6,192.26666666666665 1440,150 L 1440,600 L 0,600 Z" stroke="none" stroke-width="0" fill="url(#gradient)" fill-opacity="0.53" className="transition-all duration-300 ease-in-out delay-150 path-0"></path><defs><linearGradient id="gradient" x1="0%" y1="50%" x2="100%" y2="50%"><stop offset="5%" stop-color="#7bdcb5"></stop><stop offset="95%" stop-color="#8ED1FC"></stop></linearGradient></defs><path d="M 0,600 L 0,350 C 128.8,354.6666666666667 257.6,359.33333333333337 400,348 C 542.4,336.66666666666663 698.4000000000001,309.3333333333333 874,307 C 1049.6,304.6666666666667 1244.8,327.33333333333337 1440,350 L 1440,600 L 0,600 Z" stroke="none" stroke-width="0" fill="url(#gradient)" fill-opacity="1" className="path-1"></path></svg>
    </div>
    </div>
  );
}