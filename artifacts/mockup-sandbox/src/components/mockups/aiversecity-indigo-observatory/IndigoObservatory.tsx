import "../aiversecity-purple-yellow/BlueVariant.css";
import Current from "../aiversecity-purple-yellow/Current";
import "./IndigoObservatory.css";

export function IndigoObservatory() {
  return (
    <div className="indigo-observatory-preview">
      <Current
        className="theme-blue-yellow"
        observatoryClassName="indigo-observatory-surface"
      />
    </div>
  );
}

export default IndigoObservatory;
